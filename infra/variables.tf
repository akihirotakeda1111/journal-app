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

variable "github_org" {
    description = "GitHub organization or user name for OIDC trust policy"
    type        = string
}

variable "github_repo" {
    description = "GitHub repository name for OIDC trust policy"
    type        = string
    default     = "journal-app"
}

variable "django_webhook_url" {
    description = "Django evidence webhook URL. Override with ngrok URL for local apply."
    type        = string
    default     = null
}

variable "webhook_secret" {
    description = "Shared secret for Lambda -> Django evidence webhook Authorization header"
    type        = string
    sensitive   = true
    default     = "local-dev-webhook-secret"
}
