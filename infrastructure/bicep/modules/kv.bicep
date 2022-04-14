param baseName string
param location string


// keyvault
resource kv 'Microsoft.KeyVault/vaults@2019-09-01' = {
  name: 'kv-${baseName}'
  location: location
  properties:{
    tenantId: subscription().tenantId
    sku: {
      name: 'standard'
      family: 'A'
    }
    accessPolicies: []
  }
}

output kvOut string = kv.id
