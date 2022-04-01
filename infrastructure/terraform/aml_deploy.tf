# Resource group

module "resource_group" {
  source = "./modules/resource-group"

  location = var.location

  prefix  = var.prefix
  postfix = var.postfix

  tags = local.tags
}

# Azure Machine Learning workspace

module "aml_workspace" {
  source = "./modules/aml-workspace"

  rg_name  = module.resource_group.name
  location = module.resource_group.location

  prefix  = var.prefix
  postfix = var.postfix

  storage_account_id      = module.storage_account_aml.id
  key_vault_id            = module.key_vault.id
  application_insights_id = module.application_insights.id
  container_registry_id   = module.container_registry.id

  enable_aml_computecluster = var.enable_aml_computecluster
  storage_account_name      = module.storage_account_aml.name

  tags = local.tags
}

# Storage account

module "storage_account_aml" {
  source = "./modules/storage-account"

  rg_name  = module.resource_group.name
  location = module.resource_group.location

  prefix  = var.prefix
  postfix = "${var.postfix}aml"

  hns_enabled                         = false
  firewall_bypass                     = ["AzureServices"]
  firewall_virtual_network_subnet_ids = []

  tags = local.tags
}

# Key vault

module "key_vault" {
  source = "./modules/key-vault"

  rg_name  = module.resource_group.name
  location = module.resource_group.location

  prefix  = var.prefix
  postfix = var.postfix

  tags = local.tags
}

# Application insights

module "application_insights" {
  source = "./modules/application-insights"

  rg_name  = module.resource_group.name
  location = module.resource_group.location

  prefix  = var.prefix
  postfix = var.postfix

  tags = local.tags
}

# Container registry

module "container_registry" {
  source = "./modules/container-registry"

  rg_name  = module.resource_group.name
  location = module.resource_group.location

  prefix  = var.prefix
  postfix = var.postfix

  tags = local.tags
}