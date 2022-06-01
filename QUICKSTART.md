# Quickstart

## Technical requirements

- Github as the source control repository
- Azure DevOps as the DevOps orchestration tool
- Azure service principals to access / create Azure resources from Azure DevOps (or the ability to create them)
- Git bash or another shell script editor on your local machine
   

## Prerequisites
---

**Duration: 45min**

**Note: This demo is based on the beta version for the MLOps Azure Machine Learning Classical ML Pattern. Due to ongoing, cli v2 changes and Azure Machine Learning enhencements, the demo can fail. The team is working on keeping the example as up-to-date as possible.**


1. Create Service Principles

   For the use of the demo, the creation of two service principles is required. Go into your Azure portal to set those up.

   1.1. Select Azure Active Directory (AAC)

   ![SP1](./images/SP-setup1.png)

   1.2. Select App Registrations on the left panel, then select "new registration".

   ![PS2](./images/SP-setup2.png)

   1.3. Go through the process of creating a Service Principle (SP) selecting "Accounts in any organizational directory (Any Azure AD directory - Multitenant)" and name it  "Azure-ARM-Dev-ProjectName". Once created, repeat and create a new SP named "Azure-ARM-Prod-ProjectName". Please replace "ProjectName" with the name of your project so that the service principal can be uniquely identified. 

   1.4. Go to "Certificates & Secrets" and add for each SP "New client secret", then store the value and secret sepperately.

   1.5. Select your subscription and go to IAM. Select +Add then select "Add Role Assigment.

   ![PS3](./images/SP-setup3.png)

   1.6. Select Contributor and add members selecting + Select Members. Add the member "Azure-ARM-Dev-ProjectName" as create before.

   ![SP4](./images/SP-setup4.png)

   1.7. Repeat step with "Azure-ARM-Prod-ProjectName". The SP setup is successfully finished.


2. Set up Github Environment

   2.1. Go to https://github.com/Azure/mlops-templates/fork to fork the mlops templates repo. This repo has reusable mlops code that can be used across multiple projects. 
   
   ![image](./images/gh-fork.png)

   2.2 Go to https://github.com/Azure/mlops-project-template and click the button "Use this template" (if you don't see it, you might have to sign in to Github first). 
   
   ![Github Use Template](./images/gh-usethistemplate.png)
   
   2.3. After clicking the button you'll choose your github account/org and enter a repository name e.g. "MLOps-Project-Template", optionally a description and finally click on "Create Repository from template'". 
   
   ![Github Create new Repo](./images/gh-createnewrepo.png)
   
   2.4. Now you should have your own Github repository with the solution accelerator. Please go to the following files and replace the name field "Azure/mlops-templates" in the repositories section with "yourgithuborgname/mlops-templates".
   
   - /infrastructure/terraform/pipelines/tf-ado-deploy-infra.yml
   - /infrastructure/bicep/pipelines/bicep-ado-deploy-infra.yml
   - /classical/aml-cli-v2/mlops/devops-pipelines/deploy-batch-endpoint-pipeline.yml
   - /classical/aml-cli-v2/mlops/devops-pipelines/deploy-model-training-pipeline.yml
   - /classical/aml-cli-v2/mlops/devops-pipelines/deploy-online-endpoint-pipeline.yml
   - /classical/python-sdk/mlops/devops-pipelines/deploy-model-batch-scoring.yml
   - /classical/python-sdk/mlops/devops-pipelines/deploy-model-training-pipeline.yml

   2.5 Create an empty repository e.g. "Mlops-Test"
   
   2.6 Download this [shell script](sparse_checkout.sh). In the file, please update the variables based on the following choices:
   
   ```console
   
      infrastructure_version=terraform   #options: terraform / bicep / arm
      cicd_agent=azure-devops   #options: azure-devops or github-actions
      project_type=classical   #options: classical / computer-vision / nlp
      mlops_version=aml-cli-v2   #options: python-sdk / aml-cli-v2
      git_folder_location='<local path>'   #replace with the local root folder location where you want to create the project folder
      project_name=Mlops-Test   #replace with your project name
      github_org_name=orgname   #replace with your github org name
      project_template_github_url=https://github.com/azure/mlops-project-template   #replace with the url for the project template for your organization created in step 2.2
   
   ```
   2.7 Execute this script in Git Bash or another terminal. This will create a repo for your project which you can use in subsequent steps. In case you face any authentication issues, follow this link to authenticate yourself using an ssh key: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
   
   2.8. Next, create an SSO token in github by selecting "Developer settings" in your github account settings.

   ![GH1](./images/GH-setup1.png)
   
   2.9. Select "Personal Access Token", then generate new token. Select the check boxes and name your token "MLOpsToken". Select "Generate Token". Copy/Paste token key to a notepate interim.
   
   ![GH2](./images/GH-setup2.png)
   
   2.10. If your organization uses single sign on for Github, then click on "Authorize" the token to have access to the github organization. 
   
   ![GH3](./images/GH-setup3.png)
   
   The github setup is successfully finished.


3. Set up Azure DevOps

   3.1. Go to [Azure DevOps](https://dev.azure.com/) to set up your MLOps deployment environment. To deploy the infrastructure via ADO (Azure DevOps), you will have to have an organization and a project, with a service connection to your subscription configured.
   
   3.2. Create a new project in Azure Devops. Feel free to name it according to your project practices.
   
   ![ADO Project](./images/ADO-project.png)
   
   3.3. In the project under 'Project Settings (at the bottom of the screen when in the project)' select "Service Connections".
   
   ![ADO1](./images/ADO-setup1.png)
   
   **Azure Subscription Connection:**
   
      3.3.1 Select "New Service Connection".

      ![ADO2](./images/ADO-setup2.png)

      3.3.2 Select "Azure Resource Manager", select "Next", select "Service principal (manual)", select "Next", select your subscrption where your Service Principal is stored and name the service connection "Azure-ARM-Dev". Fill in the details of the Dev service principal created in step 1. Select "Grant access permission to all pipelines", then select "Save". Repeat this step to create another service connection "Azure-ARM-Prod" using the details of the Prod service principal created in step 1.

      ![ADO3](./images/ado-service-principal-manual.png)
      
   **Github Connection:**
   
      3.3.4 Select "New Service Connection".

      ![ADO4](./images/ADO-setup2.png)
      
      3.3.5 Select "Github", select "Next", select "Personal Access Token" and paste your Github SSO Token in the Personal Access token field, in the "Service connection name" field, enter "github-connection", grant pipeline security access, then select "Save".
      
      ![ADO5](./images/ADO-setup4.png)
      
      Repeat this step, and for the "Service connection name" enter YOUR GITHUB ORGANIZATION NAME or YOUR GITHUB NAME. Finishing this step, your conection should look like this.
   
      ![ADO6](./images/ADO-setup5.png)

   The Azure DevOps setup is successfully finished.
 
 
**This finishes the prerequisite section and the deployment of the solution accelerator can happen accordingly.**


   
## Outer Loop: Deploying Infrastructure via Azure DevOps
---
   
   1. Go to your Github cloned repo and select the "config-infra-prod.yml" file.
   
   ![ADO Run4](./images/ADO-run4.png)
   
   Under global, there's two values namespace and postfix. These values should render the names of the artifacts to create unique. Especially the name for the storage account, which has the most rigid constraints, like uniqueness Azure wide and 3-24 lowercase characters and numbers. So please change namespace and/or postfix to a value of your liking and remember to stay within the contraints of a storage account name as mentioned above. Then save, commit, push, pr to get these values into the pipeline.

   2. Go to ADO pipelines
   
   ![ADO Pipelines](./images/ADO-pipelines.png)
   
   3. Select "New Pipeline".
   
   ![ADO Run1](./images/ADO-run1.png)
   
   4. Select "Github".
   
   ![ADO Where's your code](./images/ado-wheresyourcode.png)
   
   5. Select your /MLOps-Test repository.
   
   ![ADO Run2](./images/ADO-run2.png)
   
   If your new repository is not visible, then click on the "provide access" link and on the next screen, click on the "grant" button next to the organization name to grant access to your organization.
   
   6. Select "Existing Azure Pipeline YAML File"
   
   ![ADO Run3](./images/ADO-run3.png)
   
   
   7. Select "main" as a branch and choose 'infrastructure/pipelines/tf-ado-deploy-infra.yml', then select "Continue".
   
   ![Select Infrastructure Pipeline](./images/ado-select-pipeline-yaml-file.png)
   

   
   8. Run the pipeline. This will take a few minutes to finish. The pipeline should create the following artifacts:
   * Resource Group for your Workspace including Storage Account, Container Registry, Application Insights, Keyvault and the Azure Machine Learning Workspace itself.
   * In the workspace there's also a compute cluster created.
   
   ![ADO Run5](./images/ADO-run5.png)
   
   Now the Outer Loop of the MLOps Architecture is deployed.
   
   ![ADO Run6](./images/ADO-run-infra-pipeline.png)


## Inner Loop: Deploying Classical ML Model Development / Moving to Test Environment 
---

   1. Go to ADO pipelines
   
   ![ADO Pipelines](./images/ADO-pipelines.png)

   2. Select "New Pipeline".
   
   ![ADO Run1](./images/ADO-run1.png)
   
   3. Select "Github".
   
   ![ADO Where's your code](./images/ado-wheresyourcode.png)
   
   4. Select your /MLOps-Test repository.
   
   ![ADO Run2](./images/ADO-run2.png)
   
   5. Select "Existing Azure Pipeline YAML File"
   
   ![ADO Run3](./images/ADO-run3.png)
   
   6. Select "main" as a branch and choose '/mlops/devops-pipelines/deploy-model-training-pipeline.yml', then select "Continue".  

   ![ADO Run9](./images/ADO-run9.png)
   
   >**IMPORTANT: This pipeline needs an additional connection to the Github repo yourorgname/mlops-templates, where all the templates are stored and maintained, which, like legos, encapsulate certain functionality. That's why you see in the pipeline itself a lot of calls to '-template: template in mlops-templates'. These functionalities are install the azure cli, or ml extension or run a pipeline etc. Therefore we created the connection 'github-connection' in the beginning currenly hard-coded.**
   
   This step deploys the training pipeline to the Azure Machine Learning workspace created in the previous steps. 

   Now the Inner Loop of the MLOps Architecture is deployed.
      
      
 
## Inner / Outer Loop: Moving to Production
---
   
   >**NOTE: This is an end-to-end machine learning pipeline which runs a linear regression to predict taxi fares in NYC. The pipeline is made up of components, each serving  different functions, which can be registered with the workspace, versioned, and reused with various inputs and outputs.**

   >**Prepare Data
   This component takes multiple taxi datasets (yellow and green) and merges/filters the data, and prepare the train/val and evaluation datasets.
   Input: Local data under ./data/ (multiple .csv files)
   Output: Single prepared dataset (.csv) and train/val/test datasets.**

   >**Train Model
   This component trains a Linear Regressor with the training set.
   Input: Training dataset
   Output: Trained model (pickle format)**
   
   >**Evaluate Model
   This component uses the trained model to predict taxi fares on the test set.
   Input: ML model and Test dataset
   Output: Performance of model and a deploy flag whether to deploy or not.
   This component compares the performance of the model with all previous deployed models on the new test dataset and decides whether to promote or not model into production. Promoting model into production happens by registering the model in AML workspace.**

   >**Register Model
   This component scores the model based on how accurate the predictions are in the test set.
   Input: Trained model and the deploy flag.
   Output: Registered model in Azure Machine Learning.**
   
   1. Go to ADO pipelines
   
   ![ADO Pipelines](./images/ADO-pipelines.png)

   2. Select "New Pipeline".
   
   ![ADO Run1](./images/ADO-run1.png)
   
   3. Select "Github".
   
   ![ADO Where's your code](./images/ado-wheresyourcode.png)
   
   4. Select your /MLOps-Test repository.
   
   ![ADO Run2](./images/ADO-run2.png)
   
   5. Select "Existing Azure Pipeline YAML File"
   
   ![ADO Run3](./images/ADO-run3.png)
   
   6. Select "main" as a branch and choose '/mlops/devops-pipelines/deploy-batch-endpoint.yml', then select "Continue".  
   
   ![ADO Run10](./images/ADO-run10.png)
   
   7. Batch endpoint names need to be unique, so please change "taxi-fare-batch" to another unique name and then select "Run".

   ![ADO Run11](./images/ADO-batch-pipeline.png)
   
   **IMPORTANT: If the run fails due to an existing online endpoint name, recreate the pipeline as discribed above and change "taxi-fare-batch" to "taxi-fare-batch[random number]"**
   
   8. When the run completes, you will see:
   
   ![ADO Run12](./images/ADO-run12.png)
   
  Now the Inner Loop is connected to the Outer of the MLOps Architecture and inference has been run.
  
  

## Next Steps
---

This finishes the demo according to the architectual patters: Azure Machine Learning Classical Machine Learning. Next you can dive into your Azure Machine Learning service in the Azure Portal and see the inference results of this example model. 

As the cli v2 is still in development, the following components are not part of this demo:
- Model Monitoring for Data/Model Drift
- Automated Retraining
- Model and Infrastructure triggers

As the development team builds according to the Product Groups release plan, no custom components are going to be developed rather it is intended to wait for full GA release of the cli v2 to address those components. 

Interim it is recommended to schedule the deployment pipeline for development for complete model retraining on a timed trigger.

For questions, please hand in an issue or reach out to the development team at Microsoft.


   
   
   
 
