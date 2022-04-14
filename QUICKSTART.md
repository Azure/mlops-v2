# Quickstart

## Prerequisites
---

**Note: This demo is based on the beta version for the MLOps Azure Machine Learning Classical ML Pattern. Due to ongoing, cli v2 changes and Azure Machine Learning enhencements, the demo can fail. The team is working on keeping the example as up-to-date as possible.**

1. Create Service Principles

   For the use of the demo, the creation of two service principles is required. Go into your Azure portal to set those up.

   Select Azure Active Directory (AAC)

   ![SP1](./images/SP-setup1.png)

   Select App Registrations on the left panel, then select "new registration".

   ![PS2](./images/SP-setup2.png)

   Go through the process of creating a Service Principle (SP) selecting "Accounts in any organizational directory (Any Azure AD directory - Multitenant)" and name it  "Azure-ARM-Dev". Once created, repeate and create a new SP named "Azure-ARM-Prod".

   Go to "Certificates & Secrets" and add for each SP "New client secret", then store the value and secret sepperately.

   Select your subscription and go to IAM. Select +Add then select "Add Role Assigment.

   ![PS3](./images/SP-setup3.png)

   Select Contributor and add members selecting + Select Members. Add the member "Azure-ARM-Dev" as create before.

   ![SP4](./images/SP-setup4.png)

   Repeat step with "Azure-ARM-Prod". The SP setup is successfully finished.


2. Set up Github Environment

   Goto https://github.com/Azure/mlops-v2.
   
   Click the button "Use this template" (if you don't see it, you might have to sign in to Github first). 
   
   ![Github Use Template](./images/gh-usethistemplate.png)
   
   After clicking the button you'll choose your github account/org and enter a repository name "MLOps-Test", optionally a description and finally click on "Create Repository from template'". 
   
   ![Github Create new Repo](./images/gh-createnewrepo.png)
   
   Now you should have your own Github repository with the solution accelerator.
   
   Next, create an SSO token in github by selecting "Developer settings" in your github account settings.

   ![GH1](./images/GH-setup1.png)
   
   Select "Personal Access Token", then generate new token. Select the check boxes and name your token "MLOpsToken". Select "Generate Token". Copy/Paste token key to a notepate interim.
   
   ![GH2](./images/GH-setup2.png)
   
   Now "Authorize" the token to have access to the Azure organization. If you are not a member of the Azure organization please enable it beforehand in your organisation setting.
   
   ![GH3](./images/GH-setup3.png)
   
   The github setup is successfully finished.


3. Set up Azure DevOps

   Go to [Azure DevOps](https://dev.azure.com/) to set up your MLOps deployment environment. To deploy the infrastructure via ADO (Azure DevOps), you will have to have an organization and a project, with a service connection to your subscription configured.
   
   Create a new organization and project in Azure Devops. Feel free to name both according to your project practices.
   
   ![ADO Project](./images/ADO-project.png)
   
   In the project under 'Project Settings (at the bottom of the screen when in the project)' select "Service Connections".
   
   ![ADO1](./images/ADO-setup1.png)
   
   **Azure Subscription Connection:**
   
      Select "New Service Connection".

      ![ADO2](./images/ADO-setup2.png)

      Select "Azure Resource Manager", select "Next", select "Service principal (automatic)", select "Next", select your subscrption where your SP is stored and name the service connection "Azure-ARM-Prod". Select "Grant access permission to all pipelines", then select "Save". 

      ![ADO3](./images/ADO-setup3.png)
      
   **Github Connection:**
   
      Select "New Service Connection".

      ![ADO4](./images/ADO-setup2.png)
      
      Select "Github", select "Next", select "Personal Access Token" and paste your Github SSO Token in the Personal Access token field, name the "Service connection name" accordingly "mlops-v2-service-connection", grand pipeline security access, then select "Save".
      
      ![ADO5](./images/ADO-setup4.png)
      
      If it does not exist already, repeat exactly this step only name name the "Service connection name" accordingly YOUR GITHUB NAME. Finishing this step, your conection should look like this.
   
      ![ADO6](./images/ADO-setup5.png)

   The Azure DevOps setup is successfully finished.
 
 
**This finishes the prerequisite section and the deployment of the solution accelerator can happen accordingly.**


   
## Outer Loop: Deploying Infrastructure via Azure DevOps
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
   
   6. Select "main" as a branch and choose 'infrastructure/bicep/pipelines/bicep-iac-std-pipelines.yml', then select "Continue".
   
   ![Select Infrastructure Pipeline](./images/ADO-selectinfrapipeline.png)
   
   7. **IMPORTANT: THIS STEP WILL AUTOMATED SOON** 
   
   DO NOT run the pipeline yet. Go to your Github cloned repo and select the "config-infra-prod.yml" file.
   
   ![ADO Run4](./images/ADO-run4.png)
   
   Under global, change postfix: 818 to postfix: 819 (line 8) and save.
   
   8. Now go back to ADO and "Run". This will take a few minutes to finish. The pipeline should create the following artifacts:
   * Resource Group for your Workspace including Storage Account, Container Registry, Application Insights, Keyvault and the Azure Machine Learning Workspace itself.
   * In the workspace there's also a compute cluster created.
   
   ![ADO Run5](./images/ADO-run5.png)
   
   Now the Outer Loop of the MLOps Architecture is deployed.
   
   ![ADO Run6](./images/ADO-run6.png)


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
   
   6. Select "main" as a branch and choose '/mlops/devops-pipelines/aml-cli-v2/deploy-model-training-pipeline-v2.yml', then select "Continue".  

   ![ADO choose your pipeline](./images/ADO-selectinfrapipeline.png)
   
   >**IMPORTANT: This pipeline needs an additional connection to the Github repo Azure/mlops-templates, where all the templates are stored and maintained, which, like legos, encapsulate certain functionality. That's why you see in the pipeline itself a lot of calls to '-template: template in mlops-templates'. These functionalities are install the azure cli, or ml extension or run a pipeline etc. Therefore we created the connection 'mlops-v2-service-connection' in the beginning currenly hard-coded.**
   
   7. Do to global subscription issues in Azure change "onlineendpoint1" to "onlineendpoint2", select "Run".

   ![ADO Run7](./images/ADO-run7.png)
   
   **IMPORTANT: If the run fails due to an existing online endpoint name, recreate the pipeline as discribed above and change "onlineendpoint1" to "onlineendpoint[random number]"**
   
   8. When the run completes, you will see:
   
   ![ADO Run8](./images/ADO-run8.png)

   
 
## Inner / Outer Loop: Moving to Production
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
   
   6. Select "main" as a branch and choose '/mlops/devops-pipelines/aml-cli-v2/deploy-batch-scoring-pipeline-v2.yml', then select "Continue".  
   
   
   
   
   

## Setting Variables
---

>Right now there's just a deployment from 'main' and therefore only production artifacts are deployed.

For a quickstart, the only variables needed to be set are in 'config-infra-prod.yml'(in the root of the repo):
* If your location (Azure Region) is different from 'westus' then you'll have to adjust it to the desired one p.ex. 'westus2', 'northerneurope'.
* the function of 'namespace' is to make all your artifacts, that you're going to deploy, unique. Since there's going to be a Storage Account deployed, it has to adhere to the naming limitations of these (3-24 characters, all lowercase letters or numbers)
* as of now, the 'ado_service_connection_rg:Azure-ARM-dev' needs to have contributor permission subscription wide, since there's a resource groups being created, which contains the artifacts for the Machine Learning Workspace (Storage Account, Key Vault, Application Insights, Container Registry). You then have to create a service connection in your ADO project, which has the same name ' or adjust it here accordingly.






![ADO Github Service Connection](./images/ado-ghserviceconnection.png)


With the following endresult:

![ADO Training Pipeline](./images/ado-trainingpipeline.png)
