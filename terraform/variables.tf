variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-2"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "Must be a valid IPv4 CIDR block."
  }
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "my_ip" {
  description = "IP address for SSH access (CIDR notation)"
  type        = string
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "service-registry"
}

variable "docker_image" {
  description = "Docker image name"
  type        = string
  default     = "anthonysjhenry633/service-registry:latest"
}

variable "app_secret_key" {
  description = "Application secret key"
  type        = string
  sensitive   = true
}

