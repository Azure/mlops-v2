param location string
param baseName string
param stoacctid string
param kvid string
param appinsightid string
param crid string



// azure machine learning service
resource amls 'Microsoft.MachineLearningServices/workspaces@2020-09-01-preview' = {
  name: 'mlw-${baseName}'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  sku:{
    tier: 'basic'
    name: 'basic'
  }
  properties:{
    friendlyName: 'mlw-${baseName}'
    storageAccount: stoacctid
    keyVault: kvid
    applicationInsights: appinsightid
    containerRegistry: crid
    encryption:{
      status: 'Disabled'
      keyVaultProperties:{
        keyIdentifier: ''
        keyVaultArmId: ''
      }
    }
  }

}

output amlsName string = amls.name
