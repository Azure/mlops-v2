resource "azurerm_application_insights" "adl_appi" {
  name                = "appi-${var.prefix}-${var.postfix}"
  location            = var.location
  resource_group_name = var.rg_name
  application_type    = "web"

  tags = var.tags
}