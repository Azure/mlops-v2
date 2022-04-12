resource "azurerm_machine_learning_workspace" "adl_mlw" {
  name                    = "mlw-${var.prefix}-${var.postfix}"
  location                = var.location
  resource_group_name     = var.rg_name
  application_insights_id = var.application_insights_id
  key_vault_id            = var.key_vault_id
  storage_account_id      = var.storage_account_id
  container_registry_id   = var.container_registry_id

  identity {
    type = "SystemAssigned"
  }

  tags = var.tags
}

# Compute cluster

resource "azurerm_machine_learning_compute_cluster" "adl_aml_ws_compute_cluster" {
  name                          = "mlwcc${var.prefix}${var.postfix}"
  location                      = var.location
  vm_priority                   = "LowPriority"
  vm_size                       = "STANDARD_DS2_V2"
  machine_learning_workspace_id = azurerm_machine_learning_workspace.adl_mlw.id
  count                         = var.enable_aml_computecluster ? 1 : 0

  scale_settings {
    min_node_count                       = 0
    max_node_count                       = 1
    scale_down_nodes_after_idle_duration = "PT120S" # 120 seconds
  }

  identity {
    type = "SystemAssigned"
  }
}

