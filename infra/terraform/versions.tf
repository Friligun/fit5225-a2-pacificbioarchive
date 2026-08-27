terraform {
  required_version = ">= 1.8.0"
  required_providers {
    aws      = { source = "hashicorp/aws", version = "~> 5.0" }
    alicloud = { source = "aliyun/alicloud", version = "~> 1.230" }
    random   = { source = "hashicorp/random", version = "~> 3.6" }
  }
}
provider "aws" { region = var.aws_region }
provider "alicloud" { region = var.alibaba_region }
