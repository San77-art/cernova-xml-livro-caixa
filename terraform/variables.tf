variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region"
}

variable "db_password" {
  type        = string
  sensitive   = true
  description = "Database password"
  default     = "CernovaRB2026!"
}
