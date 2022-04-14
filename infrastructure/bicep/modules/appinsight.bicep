param baseName string
param location string


// app insights
resource appinsight 'Microsoft.Insights/components@2020-02-02-preview' = {
  name: 'appi-${baseName}'
  location: location
  kind: 'web'
  properties:{
    Application_Type: 'web'
  }
}

output appinsightOut string = appinsight.id
