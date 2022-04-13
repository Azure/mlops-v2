data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "adl_kv" {
  name                = "kv-${var.prefix}-${var.postfix}"
  location            = var.location
  resource_group_name = var.rg_name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  network_acls {
    default_action             = "Deny"
    ip_rules                   = []
    virtual_network_subnet_ids = []
    bypass                     = "None"
  }

  tags = var.tags
}