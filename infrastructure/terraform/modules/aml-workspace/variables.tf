variable "rg_name" {
  type        = string
  description = "Resource group name"
}

variable "location" {
  type        = string
  description = "Location of the resource group"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "A mapping of tags which should be assigned to the deployed resource"
}

variable "prefix" {
  type        = string
  description = "Prefix for the module name"
}

variable "postfix" {
  type        = string
  description = "Postfix for the module name"
}

variable "storage_account_id" {
  type        = string
  description = "The ID of the Storage Account linked to AML workspace"
}

variable "key_vault_id" {
  type        = string
  description = "The ID of the Key Vault linked to AML workspace"
}

variable "application_insights_id" {
  type        = string
  description = "The ID of the Application Insights linked to AML workspace"
}

variable "container_registry_id" {
  type        = string
  description = "The ID of the Container Registry linked to AML workspace"
}

variable "enable_aml_computecluster" {
  description = "Variable to enable or disable AML compute cluster"
  default     = false
}

variable "storage_account_name" {
  type        = string
  description = "The Name of the Storage Account linked to AML workspace"
}