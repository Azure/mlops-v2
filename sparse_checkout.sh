infrastructure_version=terraform   #options: terraform / bicep 
project_type=cv   #options: classical / cv / nlp
mlops_version=aml-cli-v2   #options: aml-cli-v2 / python-sdk-v1 / python-sdk-v2 / rai-aml-cli-v2
orchestration=github-actions #options: github-actions / azure-devops
git_folder_location='/home/sdonohoo/projects'   #replace with the local root folder location where you want to create the project folder
project_name=gha-tf-cv   #replace with your project name
github_org_name=sdonohoo   #replace with your github org name
project_template_github_url=https://github.com/sdonohoo/mlops-project-template   #replace with the url for the project template for your organization created in step 2.2, or leave for demo purposes

cd $git_folder_location

# Clone MLOps Project repo
git clone \
  --branch 'main-dec31' \
  --depth 1  \
  --filter=blob:none  \
  --sparse \
  $project_template_github_url \
  $project_name

cd $project_name
git sparse-checkout init --cone
git sparse-checkout set infrastructure/$infrastructure_version $project_type/$mlops_version

# Move files to appropiate level
mv $project_type/$mlops_version/data-science data-science
mv $project_type/$mlops_version/mlops mlops
mv $project_type/$mlops_version/data data

if [[ "$mlops_version" == "python-sdk-v1" ]]
then
  echo "mlops_version=python-sdk-v1"
  mv $project_type/$mlops_version/config-aml.yml config-aml.yml
fi
rm -rf $project_type

mv infrastructure/$infrastructure_version $infrastructure_version
rm -rf infrastructure
mv $infrastructure_version infrastructure

if [[ "$orchestration" == "github-actions" ]]
then
  echo "github-actions"
  rm -rf mlops/devops-pipelines
  mkdir -p .github/workflows/
  mv mlops/github-actions/* .github/workflows/
  rm -rf mlops/github-actions
  mv infrastructure/github-actions/* .github/workflows/
  rm -rf infrastructure/devops-pipelines
  rm -rf infrastructure/github-actions
fi

if [[ "$orchestration" == "azure-devops" ]]
then
  echo "azure-devops"
  rm -rf mlops/github-actions
  rm -rf infrastructure/github-actions
fi

# Upload to custom repo in Github
rm -rf .git
git init -b main

gh repo create $project_name --private

app=($(az ad app create --display-name gha-tf-cv --query "[appId,id]" -o tsv | tr -d '\r'))
spId=$(az ad sp create --id ${app[0]} --query id -o tsv)
subId=$(az account show --query id -o tsv)

#az role assignment create --role owner --assignee-object-id  $spId --assignee-principal-type ServicePrincipal --scope /subscriptions/$subId/resourceGroups/az-k8s-ht68-rg
az role assignment create --role owner --assignee-object-id  $spId --assignee-principal-type ServicePrincipal --scope /subscriptions/$subId


# Create a new federated identity credential
az rest --method POST --uri "https://graph.microsoft.com/beta/applications/${app[1]}/federatedIdentityCredentials" --body "{\"name\":\"gha-tf-cv-main-gh\",\"issuer\":\"https://token.actions.githubusercontent.com\",\"subject\":\"repo:sdonohoo/gha-tf-cv:ref:refs/heads/main\",\"description\":\"Access to branch main\",\"audiences\":[\"api://AzureADTokenExchange\"]}"

# Set Secrets
gh secret set --repo https://github.com/sdonohoo/gha-tf-cv AZURE_CLIENT_ID -b ${app[0]}
gh secret set --repo https://github.com/sdonohoo/gha-tf-cv AZURE_TENANT_ID -b $(az account show --query tenantId -o tsv)
gh secret set --repo https://github.com/sdonohoo/gha-tf-cv AZURE_SUBSCRIPTION_ID -b $subId
#gh secret set --repo https://github.com/sdonohoo/gha-tf-cv USER_OBJECT_ID -b $spId

# Create credentials for deployment
#SP=$(az ad sp create-for-rbac --name azcred_gha_tf --role contributor --scopes /subscriptions/11213db9-7bfe-4b6b-84af-df180008a813 --sdk-auth)
#echo $SP | gh secret set AZURE_CREDENTIALS -R $github_org_name/$project_name -a actions
#echo $SP | awk -F: 'BEGIN{FS=OFS="[:,]"} $1~"clientId" {print $2}' | gh secret set ARM_CLIENT_ID -R $github_org_name/$project_name -a actions
#echo $SP | awk -F: 'BEGIN{FS=OFS="[:,]"} $1~"clientSecret" {print $2}' | gh secret set ARM_CLIENT_SECRET -R $github_org_name/$project_name -a actions
#echo $SP | awk -F: 'BEGIN{FS=OFS="[:,]"} $1~"subscriptionId" {print $2}' | gh secret set ARM_SUBSCRIPTION_ID -R $github_org_name/$project_name -a actions
#echo $SP | awk -F: 'BEGIN{FS=OFS="[:,]"} $1~"tenantId" {print $2}' | gh secret set ARM_TENANT_ID -R $github_org_name/$project_name -a actions

git remote add origin git@github.com:$github_org_name/$project_name.git
git add . && git commit -m 'initial commit'
git push --set-upstream origin main
