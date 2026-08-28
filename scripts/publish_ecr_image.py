"""Publish a local Docker image to ECR without depending on Docker Desktop's proxy."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError


CHUNK_SIZE = 10 * 1024 * 1024
RETRIES = 5
CONFIG_MEDIA_TYPE = "application/vnd.docker.container.image.v1+json"
LAYER_MEDIA_TYPE = "application/vnd.docker.image.rootfs.diff.tar.gzip"
MANIFEST_MEDIA_TYPE = "application/vnd.docker.distribution.manifest.v2+json"


def sha256_file(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as source:
        while chunk := source.read(CHUNK_SIZE):
            digest.update(chunk)
            size += len(chunk)
    return f"sha256:{digest.hexdigest()}", size


def retry(label: str, operation):
    for attempt in range(1, RETRIES + 1):
        try:
            return operation()
        except (BotoCoreError, ClientError) as error:
            if attempt == RETRIES:
                raise
            wait_seconds = 2**attempt
            print(f"{label} interrupted ({error}); retrying in {wait_seconds}s", flush=True)
            time.sleep(wait_seconds)


def ensure_layer(ecr, repository: str, blob: Path, digest: str, size: int) -> None:
    available = retry(
        "Checking layer",
        lambda: ecr.batch_check_layer_availability(
            repositoryName=repository, layerDigests=[digest]
        ),
    )["layers"]
    if any(layer.get("layerAvailability") == "AVAILABLE" for layer in available):
        print(f"Reusing {digest[:19]} ({size / 1024 / 1024:.1f} MiB)", flush=True)
        return

    upload = retry(
        "Starting layer upload",
        lambda: ecr.initiate_layer_upload(repositoryName=repository),
    )
    upload_id = upload["uploadId"]
    print(f"Uploading {digest[:19]} ({size / 1024 / 1024:.1f} MiB)", flush=True)
    with blob.open("rb") as source:
        offset = 0
        while chunk := source.read(CHUNK_SIZE):
            last_byte = offset + len(chunk) - 1
            retry(
                f"Uploading bytes {offset}-{last_byte}",
                lambda offset=offset, last_byte=last_byte, chunk=chunk: ecr.upload_layer_part(
                    repositoryName=repository,
                    uploadId=upload_id,
                    partFirstByte=offset,
                    partLastByte=last_byte,
                    layerPartBlob=chunk,
                ),
            )
            offset = last_byte + 1
    retry(
        "Completing layer upload",
        lambda: ecr.complete_layer_upload(
            repositoryName=repository, uploadId=upload_id, layerDigests=[digest]
        ),
    )


def gzip_member(archive: tarfile.TarFile, member_name: str, destination: Path) -> tuple[str, int]:
    member = archive.getmember(member_name)
    source = archive.extractfile(member)
    if source is None:
        raise RuntimeError(f"Could not read Docker archive member: {member_name}")
    with source:
        prefix = source.read(2)
        if prefix == b"\x1f\x8b":
            # OCI image archives already contain registry-ready gzip layers.
            with destination.open("wb") as compressed:
                compressed.write(prefix)
                shutil.copyfileobj(source, compressed, length=CHUNK_SIZE)
        else:
            with destination.open("wb") as raw:
                with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=1) as compressed:
                    compressed.write(prefix)
                    shutil.copyfileobj(source, compressed, length=CHUNK_SIZE)
    with gzip.open(destination, "rb") as compressed:
        with tarfile.open(fileobj=compressed, mode="r:") as layer:
            for _ in layer:
                pass
    return sha256_file(destination)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Local image name, for example pacificbio-api:local")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--region", default="ap-southeast-2")
    parser.add_argument("--public", action="store_true", help="Publish to Amazon ECR Public")
    args = parser.parse_args()

    # The workstation's Docker Desktop proxy is unreliable for large ECR uploads.
    for name in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
        os.environ.pop(name, None)
    os.environ["NO_PROXY"] = "*"
    os.environ["no_proxy"] = "*"
    ecr = boto3.client(
        "ecr-public" if args.public else "ecr",
        region_name=args.region,
        config=Config(proxies={}, retries={"max_attempts": RETRIES, "mode": "standard"}, connect_timeout=15, read_timeout=120),
    )

    with tempfile.TemporaryDirectory(prefix="pacificbio-ecr-") as temp_dir:
        archive_path = Path(temp_dir) / "image.tar"
        subprocess.run(["docker", "save", "--output", str(archive_path), args.image], check=True)
        with tarfile.open(archive_path, "r") as archive:
            manifest = json.load(archive.extractfile("manifest.json"))[0]
            config_name = manifest["Config"]
            config_blob = Path(temp_dir) / "config.json"
            config_blob.write_bytes(archive.extractfile(config_name).read())
            config_digest, config_size = sha256_file(config_blob)
            ensure_layer(ecr, args.repository, config_blob, config_digest, config_size)

            layers = []
            for index, layer_name in enumerate(manifest["Layers"]):
                layer_blob = Path(temp_dir) / f"layer-{index}.tar.gz"
                digest, size = gzip_member(archive, layer_name, layer_blob)
                ensure_layer(ecr, args.repository, layer_blob, digest, size)
                layers.append({"mediaType": LAYER_MEDIA_TYPE, "size": size, "digest": digest})

        image_manifest = json.dumps(
            {
                "schemaVersion": 2,
                "mediaType": MANIFEST_MEDIA_TYPE,
                "config": {"mediaType": CONFIG_MEDIA_TYPE, "size": config_size, "digest": config_digest},
                "layers": layers,
            },
            separators=(",", ":"),
        )
        result = retry(
            "Publishing image manifest",
            lambda: ecr.put_image(
                repositoryName=args.repository,
                imageTag=args.tag,
                imageManifest=image_manifest,
                imageManifestMediaType=MANIFEST_MEDIA_TYPE,
            ),
        )
    print(result["image"]["imageId"]["imageDigest"], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
