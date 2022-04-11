terraform {
  backend "azurerm" {} 
  required_providers {
    azurerm = {
      version = "= 2.99.0"
    }
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_client_config" "current" {}

data "http" "ip" {
  url = "https://ifconfig.me"
}