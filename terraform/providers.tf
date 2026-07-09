terraform {
  required_version = ">= 1.9"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "rg-devinsights-tfstate"
    storage_account_name = "stdevinsightstf001"
    container_name       = "tfstate"
    key                  = "devinsights.tfstate"
  }
}

provider "azurerm" {
  features {}
}
