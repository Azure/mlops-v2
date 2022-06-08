infrastructure_version=terraform   #options: terraform / bicep 
project_type=classical   #options: classical / cv
mlops_version=aml-cli-v2   #options: python-sdk / aml-cli-v2
git_folder_location='<local path>'   #replace with the local root folder location where you want to create the project folder
project_name=Mlops-Test   #replace with your project name
github_org_name=orgname   #replace with your github org name
project_template_github_url=https://github.com/azure/mlops-project-template   #replace with the url for the project template for your organization created in step 2.2, or leave for demo purposes

cd $git_folder_location

git clone \
  --depth 1  \
  --filter=blob:none  \
  --sparse \
  $project_template_github_url \
  $project_name

cd $project_name
git sparse-checkout init --cone
git sparse-checkout set infrastructure/$infrastructure_version $project_type/$mlops_version

mv $project_type/$mlops_version/data-science data-science
mv $project_type/$mlops_version/mlops mlops
mv $project_type/$mlops_version/data data

if [[ "$mlops_version" == "python-sdk" ]]
then
  echo "python-sdk"
  mv $project_type/$mlops_version/config-aml.yml config-aml.yml
fi

rm -rf $project_type

mv infrastructure/$infrastructure_version $infrastructure_version
rm -rf infrastructure
mv $infrastructure_version infrastructure

rm -rf .git
git init -b main
git remote add origin git@github.com:$github_org_name/$project_name.git
git add . && git commit -m 'initial commit'
git push --set-upstream origin main
