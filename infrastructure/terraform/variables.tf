variable "location" {
  type        = string
  description = "Location of the resource group and modules"
}

variable "prefix" {
  type        = string
  description = "Prefix for module names"
}

resource "random_string" "postfix" {
  length  = 6
  special = false
  upper   = false
}