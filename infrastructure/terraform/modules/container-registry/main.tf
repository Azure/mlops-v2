locals {
  safe_prefix  = replace(var.prefix, "-", "")
  safe_postfix = replace(var.postfix, "-", "")
}

resource "azurerm_container_registry" "adl_cr" {
  name                = "cr${local.safe_prefix}${local.safe_postfix}"
  resource_group_name = var.rg_name
  location            = var.location
  sku                 = "Premium"
  admin_enabled       = false

  network_rule_set {
    default_action  = "Deny"
    ip_rule         = []
    virtual_network = []
  }

  tags = var.tags
}