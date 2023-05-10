repo_name=$1
project_type=$2
mlops_version=$3
template_repo=$4
#infrastructure_version=bicep #options: terraform / bicep 
infrastructure_version=$5 #options: terraform / bicep 

git config --global user.email "hosted.agent@dev.azure.com"
git config --global user.name "Azure Pipeline"

mkdir files_to_keep
mkdir files_to_delete

cd $template_repo
cp --parents -r infrastructure/$infrastructure_version ../files_to_keep
cp --parents -r $project_type/$mlops_version ../files_to_keep
cp config-infra-dev.yml ../files_to_keep
cp config-infra-prod.yml ../files_to_keep
cd ..
mv $template_repo/* files_to_delete

cd $repo_name
git checkout -b main
cd ..
rm $repo_name/*
mv files_to_keep/* $repo_name
cd $repo_name

# Move files to appropiate level
mv $project_type/$mlops_version/data-science data-science
mv $project_type/$mlops_version/mlops mlops
mv $project_type/$mlops_version/data data

if [[ "$mlops_version" == "python-sdk" ]]
then
  echo "python-sdk"
  mv $project_type/$mlops_version/config-aml.yml config-aml.yml
fi

rm -rf $project_type
rm -rf mlops/github-actions

mv infrastructure/$infrastructure_version $infrastructure_version
rm -rf infrastructure
mv $infrastructure_version infrastructure

git add . && git commit -m 'initial commit'
git remote -v
git push --set-upstream origin main
