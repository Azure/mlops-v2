echo "Setting variables..."
# Set variables.
GROUP="cody-mlops-v2-test"
LOCATION="eastus"
WORKSPACE="main"
SECRET_NAME="AZ_CREDS"
COMPUTE_NAME="cpu-cluster"
SUBSCRIPTION=$(az account show --query id -o tsv)

echo "Installing Azure CLI extension for Azure Machine Learning..."
# Install ML extension for Azure CLI.
az extension add -n ml -y

echo "Creating resource group..."
# Create resource group.
az group create -n $GROUP -l $LOCATION

echo "Creating service principal and setting repository secret..."
# Set GitHub repository secret.
az ad sp create-for-rbac --name $GROUP --role contributor --scopes /subscriptions/$SUBSCRIPTION/resourceGroups/$GROUP --sdk-auth | gh secret set $SECRET_NAME

echo "Creating Azure Machine Learning workspace..."
# Create Azure Machine Learning workspace.
az ml workspace create -n $WORKSPACE -g $GROUP -l $LOCATION

echo "Configuring Azure CLI defaults..."
# Configure Azure CLI defaults.
az configure --defaults group=$GROUP workspace=$WORKSPACE location=$LOCATION

echo "Creating Azure Machine Learning compute..."
# Create Azure Machine Learning compute.
az ml compute create -n $COMPUTE_NAME --type amlcompute --min-instances 0 --max-instances 8
