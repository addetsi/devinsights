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

resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

resource "azurerm_storage_account" "landing" {
  name                     = "st${var.project}${var.environment}${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  tags                     = local.common_tags
}

resource "azurerm_storage_container" "raw" {
  name               = "raw"
  storage_account_id = azurerm_storage_account.landing.id
}

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "main" {
  name                       = "kv-${var.project}-${random_string.suffix.result}"
  resource_group_name        = azurerm_resource_group.main.name
  location                   = azurerm_resource_group.main.location
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  enable_rbac_authorization  = true
  purge_protection_enabled   = false
  soft_delete_retention_days = 7
  tags                       = local.common_tags
}

resource "azurerm_role_assignment" "kv_admin" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_eventhub_namespace" "main" {
  name                = "evhn-${var.project}-${var.environment}-${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
  capacity            = 1
  tags                = local.common_tags
}

resource "azurerm_eventhub" "github" {
  name              = "github-events"
  namespace_id      = azurerm_eventhub_namespace.main.id
  partition_count   = 2
  message_retention = 1
}

resource "azurerm_eventhub_authorization_rule" "producer" {
  name                = "producer"
  namespace_name      = azurerm_eventhub_namespace.main.name
  eventhub_name       = azurerm_eventhub.github.name
  resource_group_name = azurerm_resource_group.main.name
  listen              = false
  send                = true
  manage              = false
}

resource "azurerm_eventhub_authorization_rule" "consumer" {
  name                = "consumer"
  namespace_name      = azurerm_eventhub_namespace.main.name
  eventhub_name       = azurerm_eventhub.github.name
  resource_group_name = azurerm_resource_group.main.name
  listen              = true
  send                = false
  manage              = false
}


resource "azurerm_key_vault_secret" "eventhub_producer" {
  name         = "eventhub-producer-connection"
  value        = azurerm_eventhub_authorization_rule.producer.primary_connection_string
  key_vault_id = azurerm_key_vault.main.id

  depends_on = [azurerm_role_assignment.kv_admin]
}

resource "azurerm_key_vault_secret" "eventhub_consumer" {
  name         = "eventhub-consumer-connection"
  value        = azurerm_eventhub_authorization_rule.consumer.primary_connection_string
  key_vault_id = azurerm_key_vault.main.id

  depends_on = [azurerm_role_assignment.kv_admin]
}


resource "random_password" "sql_admin" {
  length           = 24
  special          = true
  override_special = "!#$%&*()-_=+[]{}"
}

resource "azurerm_mssql_server" "main" {
  name                         = "sql-${var.project}-${var.environment}-${random_string.suffix.result}"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = azurerm_resource_group.main.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = random_password.sql_admin.result
  tags                         = local.common_tags
}

resource "azurerm_mssql_database" "main" {
  name      = "sqldb-${var.project}-${var.environment}"
  server_id = azurerm_mssql_server.main.id
  sku_name  = "Basic"
  tags      = local.common_tags
}

resource "azurerm_key_vault_secret" "sql_admin_password" {
  name         = "sql-admin-password"
  value        = random_password.sql_admin.result
  key_vault_id = azurerm_key_vault.main.id

  depends_on = [azurerm_role_assignment.kv_admin]
}

resource "azurerm_key_vault_secret" "sql_connection_string" {
  name         = "sql-connection-string"
  value        = "Server=tcp:${azurerm_mssql_server.main.fully_qualified_domain_name},1433;Database=${azurerm_mssql_database.main.name};User ID=sqladmin;Password=${random_password.sql_admin.result};Encrypt=true;"
  key_vault_id = azurerm_key_vault.main.id

  depends_on = [azurerm_role_assignment.kv_admin]
}

resource "azurerm_mssql_firewall_rule" "allow_azure" {
  name             = "AllowAzureServices"
  server_id        = azurerm_mssql_server.main.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

resource "azurerm_mssql_firewall_rule" "allow_my_ip" {
  name             = "AllowMyIP"
  server_id        = azurerm_mssql_server.main.id
  start_ip_address = "141.93.243.1"
  end_ip_address   = "141.93.243.1"
}
