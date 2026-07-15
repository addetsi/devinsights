output "resource_group_name" {
  description = "Name of the main resource group"
  value       = azurerm_resource_group.main.name
}

output "storage_account_name" {
  description = "Name of the landing zone storage account"
  value       = azurerm_storage_account.landing.name
}

output "key_vault_name" {
  description = "Name of the Key Vault"
  value       = azurerm_key_vault.main.name
}

output "eventhub_namespace_name" {
  description = "Name of the Event Hubs namespace"
  value       = azurerm_eventhub_namespace.main.name
}

output "eventhub_name" {
  description = "Name of the Event Hub"
  value       = azurerm_eventhub.github.name
}
