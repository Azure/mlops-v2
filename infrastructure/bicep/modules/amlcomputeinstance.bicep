param location string
param baseName string
param env string
param computeInstanceName string = '${env}-${baseName}-ci'
param workspaceName string

resource amlci 'Microsoft.MachineLearningServices/workspaces/computes@2020-09-01-preview' = {
  name: '${workspaceName}/${computeInstanceName}'
  location: location
  properties:{
    computeType: 'AmlCompute'
    properties:{
      vmSize: 'Standard_DS3_v2'
      subnet: json('null')
      osType:'Linux'
      scaleSettings:{
        maxNodeCount: 4
        minNodeCount: 0

      }
    }
    
  }
}

