targetScope='subscription'

param location string = 'westus2'
param env string 
param prefix string 
param postfix string



var baseName  = '${prefix}-${postfix}${env}'
var resourceGroupName = 'rg-${baseName}'

resource resgrp 'Microsoft.Resources/resourceGroups@2020-06-01' = {
  name: resourceGroupName
  location: location
}


// storage account
module stoacct './modules/stoacct.bicep' = {
  name: 'stoacct'
  scope: resourceGroup(resgrp.name)
  params: {
    baseName: '${prefix}${postfix}${env}'
    location: location
  }
}


// keyvault
module kv './modules/kv.bicep' = {
  name: 'kv'
  scope: resourceGroup(resgrp.name)
  params:{
    location: location
    baseName: baseName
  }
}


// appinsights
module appinsight './modules/appinsight.bicep' = {
  name: 'appinsight'
  scope: resourceGroup(resgrp.name)
  params:{
    baseName: baseName
    location: location
  }
}

// container registry
module cr './modules/cr.bicep' = {
  name: 'cr'
  scope: resourceGroup(resgrp.name)
  params:{
    baseName: '${prefix}${postfix}${env}'
    location: location
  }
}


// amls workspace
module amls './modules/amls.bicep' = {
  name: 'amls'
  scope: resourceGroup(resgrp.name)
  params:{
    baseName: baseName
    location: location
    stoacctid: stoacct.outputs.stoacctOut
    kvid: kv.outputs.kvOut
    appinsightid: appinsight.outputs.appinsightOut
    crid: cr.outputs.crOut
    
  }
}


// aml compute instance
module amlci './modules/amlcomputeinstance.bicep' = {
  name: 'amlci'
  scope: resourceGroup(resgrp.name)
  params:{
    location: location
    workspaceName: amls.outputs.amlsName
  }
}
