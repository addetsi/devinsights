variable "project" {
  description = "Project name, used for tagging and naming"
  type        = string
  default     = "devinsights"
}

variable "environment" {
  description = "Deployment environment, used for tagging and naming (eg: dev, prd, nonprd)"
  type        = string
  default     = "dev"
}

variable "location" {
  description = "Azure region to deploy resources"
  type        = string
  default     = "westeurope"
}
