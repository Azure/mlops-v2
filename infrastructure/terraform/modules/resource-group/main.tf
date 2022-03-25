resource "azurerm_resource_group" "adl_rg" {
  name     = "rg-${var.prefix}-${var.postfix}"
  location = var.location
  tags     = var.tags
}