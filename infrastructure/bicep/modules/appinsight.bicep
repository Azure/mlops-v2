param baseName string
param env string
param location string


// app insights
resource appinsight 'Microsoft.Insights/components@2020-02-02-preview' = {
  name: '${env}${baseName}-appin'
  location: location
  kind: 'web'
  properties:{
    Application_Type: 'web'
  }
}

output appinsightOut string = appinsight.id
