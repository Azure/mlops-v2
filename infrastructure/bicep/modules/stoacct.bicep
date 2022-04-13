param env string
param baseName string
param location string


// stroage account
resource stoacct 'Microsoft.Storage/storageAccounts@2019-04-01' = {
  name: '${env}${baseName}sa'
  location: location
  sku:{
    name:'Standard_LRS'
  }
  kind: 'StorageV2'
  properties:{
    encryption:{
      services:{
        blob:{
          enabled: true
        }
        file:{
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'
    }
    supportsHttpsTrafficOnly: true
  }
}

output stoacctOut string = stoacct.id
