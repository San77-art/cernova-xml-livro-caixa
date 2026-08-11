terraform {
  required_version = ">= 1.0"
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

resource "aws_db_instance" "cernova" {
  identifier            = "cernova-rb-db"
  engine                = "postgres"
  engine_version        = "18.3"
  instance_class        = "db.t3.micro"
  allocated_storage     = 20
  storage_type          = "gp3"
  db_name               = "cernova_rb"
  username              = "postgres"
  password              = var.db_password
  publicly_accessible   = true
  skip_final_snapshot   = true
  
  tags = {
    Name = "cernova-rb-database"
  }
}

resource "aws_ecs_cluster" "cernova" {
  name = "cernova-rb-cluster"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
  tags = {
    Name = "cernova-rb-cluster"
  }
}

output "rds_endpoint" {
  value = aws_db_instance.cernova.endpoint
}

output "rds_database" {
  value = aws_db_instance.cernova.db_name
}

output "rds_username" {
  value = aws_db_instance.cernova.username
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.cernova.name
}
