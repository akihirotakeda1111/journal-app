variable "region" {
    description = "AWS region"
    type        = string
    default     = "ap-northeast-1"
}

variable "project" {
    description = "Project prefix"
    type        = string
    default     = "journal-app"
}

variable "domain_name" {
    description = "Domain name"
    type        = string
    default     = "a-t-dev.com"
}

variable "ssh_allowed_ip" {
    description = "IP allowed to SSH into EC2"
    type        = string
}

variable "db_name" {
    description = "App DB name"
    type        = string
    default     = "appdb"
}

variable "db_user" {
    description = "App DB user"
    type        = string
    default     = "appuser"
}

variable "db_password" {
    description = "PostgreSQL master password"
    type        = string
    sensitive   = true
}
