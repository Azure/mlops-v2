data "azurerm_client_config" "current" {}

data "http" "ip" {
  url = "https://ifconfig.me"
}

locals {
  safe_prefix  = replace(var.prefix, "-", "")
  safe_postfix = replace(var.postfix, "-", "")
}

resource "azurerm_storage_account" "adl_st" {
  name                     = "st${local.safe_prefix}${local.safe_postfix}"
  resource_group_name      = var.rg_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = var.hns_enabled

  tags = var.tags
}

resource "azurerm_role_assignment" "st_role_admin_c" {
  scope                = azurerm_storage_account.adl_st.id
  role_definition_name = "Contributor"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "st_role_admin_sbdc" {
  scope                = azurerm_storage_account.adl_st.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = data.azurerm_client_config.current.object_id
}

# Virtual Network & Firewall configuration

resource "azurerm_storage_account_network_rules" "firewall_rules" {
  resource_group_name  = var.rg_name
  storage_account_name = azurerm_storage_account.adl_st.name

  default_action             = "Deny"
  ip_rules                   = [data.http.ip.body]
  virtual_network_subnet_ids = var.firewall_virtual_network_subnet_ids
  bypass                     = var.firewall_bypass
}
