param location string
param baseName string
param env string
param stoacctid string
param kvid string
param appinsightid string
param crid string



// azure machine learning service
resource amls 'Microsoft.MachineLearningServices/workspaces@2020-09-01-preview' = {
  name: '${env}${baseName}-ws'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  sku:{
    tier: 'basic'
    name: 'basic'
  }
  properties:{
    friendlyName: '${env}${baseName}-ws'
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
