param env string
param baseName string
param location string

resource cr 'Microsoft.ContainerRegistry/registries@2020-11-01-preview' = {
  name: '${env}${baseName}cr'
  location: location
  sku: {
    name: 'Standard'
  }

  properties:{
    adminUserEnabled:true
  }
}

output crOut string = cr.id
