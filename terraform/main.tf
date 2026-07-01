locals {
  name_prefix = "${var.project}-${var.environment}"
  common_tags = {
    project     = "DevInsights"
    environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "azurerm_resource_group" "main" {
  name     = "rg-${local.name_prefix}"
  location = var.location
  tags     = local.common_tags
}
