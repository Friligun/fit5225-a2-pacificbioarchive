terraform {
  required_version = ">= 1.8.0"

  backend "s3" {
    bucket         = "pacificbio-tfstate-748998941962-20260828"
    key            = "fit5225-a2-pacificbioarchive/terraform.tfstate"
    region         = "ap-southeast-2"
    encrypt        = true
    use_lockfile   = true
    use_path_style = true
  }

  required_providers {
    aws      = { source = "hashicorp/aws", version = "~> 5.0" }
    alicloud = { source = "aliyun/alicloud", version = "~> 1.230" }
    random   = { source = "hashicorp/random", version = "~> 3.6" }
  }
}
provider "aws" { region = var.aws_region }
provider "alicloud" { region = var.alibaba_region }
