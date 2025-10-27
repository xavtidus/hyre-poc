# infra/main.tf
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# === VARIABLES ===
variable "aws_region" { default = "ap-southeast-2" }
variable "cluster_name" { default = "hyre-ai-prod" }

variable "openai_api_key" {
  type      = string
  sensitive = true
}

variable "pinecone_api_key" {
  type      = string
  sensitive = true
}

# === EKS CLUSTER ===
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name                    = var.cluster_name
  cluster_version                 = "1.29"
  subnet_ids                      = module.vpc.private_subnets
  vpc_id                          = module.vpc.vpc_id

  eks_managed_node_groups = {
    core = {
      desired_size = 2
      min_size     = 1
      max_size     = 3
      instance_types = ["t3.medium"]
    }
  }
}

# === VPC ===
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "hyre-vpc"
  cidr = "10.0.0.0/16"
  azs  = ["${var.aws_region}a", "${var.aws_region}b"]

  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true
}

# === SECRETS MANAGER ===
resource "aws_secretsmanager_secret" "hyre_secrets" {
  name = "hyre-ai-secrets"
}

resource "aws_secretsmanager_secret_version" "hyre_secrets" {
  secret_id = aws_secretsmanager_secret.hyre_secrets.id
  secret_string = jsonencode({
    OPENAI_API_KEY   = var.openai_api_key
    PINECONE_API_KEY = var.pinecone_api_key
  })
}

# === OUTPUTS ===
output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}