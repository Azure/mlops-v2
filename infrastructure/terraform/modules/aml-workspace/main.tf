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

# Datastore

resource "azurerm_resource_group_template_deployment" "arm_aml_create_datastore" {
  name                = "arm_aml_create_datastore"
  resource_group_name = var.rg_name
  deployment_mode     = "Incremental"
  parameters_content = jsonencode({
    "WorkspaceName" = {
      value = azurerm_machine_learning_workspace.adl_mlw.name
    },
    "StorageAccountName" = {
      value = var.storage_account_name
    }
  })

  depends_on = [time_sleep.wait_30_seconds]

  template_content = <<TEMPLATE
{
  "$schema": "http://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
        "WorkspaceName": {
            "type": "String"
        },
        "StorageAccountName": {
            "type": "String"
        }
    },
  "resources": [
        {
            "type": "Microsoft.MachineLearningServices/workspaces/datastores",
            "apiVersion": "2021-03-01-preview",
            "name": "[concat(parameters('WorkspaceName'), '/default')]",
            "dependsOn": [],
            "properties": {
                "contents": {
                    "accountName": "[parameters('StorageAccountName')]",
                    "containerName": "default",
                    "contentsType": "AzureBlob",
                    "credentials": {
                      "credentialsType": "None"
                    },
                    "endpoint": "core.windows.net",
                    "protocol": "https"
                  },
                  "description": "Default datastore for mlops-tabular",
                  "isDefault": false,
                  "properties": {
                    "ServiceDataAccessAuthIdentity": "None"
                  },
                  "tags": {}
                }
        }
  ]
}
TEMPLATE
}

resource "time_sleep" "wait_30_seconds" {

  depends_on = [
    azurerm_machine_learning_workspace.adl_mlw
  ]

  create_duration = "30s"
}