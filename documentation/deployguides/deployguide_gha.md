# Deployment Guide using Github Repositories Workflows

## Technical requirements

- Github as the source control repository
- Github Actions as the DevOps orchestration tool
- [GitHub client](https://cli.github.com/)
- [Azure CLI ](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- The [Terraform extension for Azure DevOps](https://marketplace.visualstudio.com/items?itemName=ms-devlabs.custom-terraform-tasks) if you are using Azure DevOps + Terraform to spin up infrastructure
- Azure service principals to access / create Azure resources from Azure DevOps or Github Actions (or the ability to create them)
- Git bash, [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) or another shell script runner on your local machine
-  When using WSL, 
   -  make sure to completely work in the context of the unix env (cloning of the repo, defining the file paths,...). You can then connect to this environment with VSCode (if that is your editor) if you install the ["Remote - SSH"](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extension
   - dos2unix: `sudo apt-get install dos2unix`
   - set up GitHub cli (mentioned above) (or via `sudo apt-get install gh`)
    - Login to GitHub: `gh auth login`
    - Config Git locally: `git config --global user.email "you@example.com"` and `git config --global user.name "Your Name"`
    - 
>**Note:**
>
>**Git version 2.27 or newer is required. See [these instructions](https://github.com/cli/cli/blob/trunk/docs/install_linux.md#debian-ubuntu-linux-raspberry-pi-os-apt) to upgrade.**

   

## Configure The GitHub Environment
---


1. **Replicate MLOps-V2 Template Repositories in your GitHub organization**  
   Go to https://github.com/Azure/mlops-templates/fork to fork the mlops templates repo into your Github org. This repo has reusable mlops code that can be used across multiple projects. 

   ![image](./images/gh-fork.png)

   Go to https://github.com/Azure/mlops-project-template/generate to create a repository in your Github org using the mlops-project-template. This is the monorepo that you will use to pull example projects from in a later step. 

   ![image](./images/gh-generate.png)

2. **Clone the mlops-v2 repository to local system**  
   On your local machine, select or create a root directory (ex: 'mlprojects') to hold your project repository as well as the mlops-v2 repository. Change to this directory.

   Clone the mlops-v2 repository to this directory. This provides the documentation and the `sparse_checkout.sh` script. This repository and folder will be used to bootstrap your projects:  
   `# git clone https://github.com/Azure/mlops-v2.git` 

3. **Configure and run sparse checkout**  
   From your local project root directory, open the `/mlops-v2/sparse_checkout.sh` for editing. Edit the following variables as needed to select the infastructure management tool used by your organization, the type of Open this file in an editor and set the following variables:
   
   >**Note:**
> When running the script through a  "vanilla" WSL, then you'll most likely get strange errors... In that case it might suffice to use dos2unix on the file
> (in WSL) run; `dos2unix sparse_checkout.sh` (in the mlops-v2 repo folder)
   

   * **infrastructure_version** selects the tool that will be used to deploy cloud resources.
   * **project_type** selects the AI workload type for your project (classical ml, computer vision, or nlp)
   * **mlops_version** selects your preferred interaction approach with Azure Machine Learning
   * **git_folder_location** points to the root project directory to which you cloned mlops-v2 in step 3
   * **project_name** is the name (case sensitive) of your project. A  GitHub repository will be created with this name
   * **github_org_name** is your GitHub organization (or GitHub username)
   * **project_template_github_url** is the URL to the original or your generated clone of the mlops_project_template repository from step 1
   * **orchestration** specifies the CI/CD orchestration to use
   <br><br>
   A sparse_checkout.sh example is below:  

   ```bash
      #options: terraform / bicep
      infrastructure_version=terraform

      #options: classical / cv / nlp
      project_type=classical
      
      #options: python-sdk / aml-cli-v2
      mlops_version=aml-cli-v2   
      
      #replace with the local root folder location where you want
      git_folder_location='/home/<username>/mlprojects'    
      
      #replace with your project name
      project_name=taxi-fare-regression   
      
      #replace with your github org name
      github_org_name=<orgname>
      
      #replace with the url for the project template for your organization created in step 2.2
      project_template_github_url=https://github.com/azure/mlops-project-template   
      
      #options: github-actions / azure-devops
      orchestration=github-actions 
   ```
   Currently, the following pipelines are supported:
   - classical 
   - cv (computer-vision) 
   - nlp (natural language processing)

4. **Run sparse checkout**  
   The `sparse_checkout.sh` script will use ssh to authenticate to your GitHub organization. If this is not yet configured in your environment, follow the steps below or refer to the documentation at  [GitHub Key Setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).
   
   > **GitHub Key Setup**
   >
   > On your local machine, create a new ssh key:  
   > `# ssh-keygen -t ed25519 -C "<your_email@example.com>"`  
   > You may press enter to all three prompts to create a new key in `/home/<username>/.ssh/id_ed25519`
   >
   > Add your SSH key to your SSH agent:  
   > `# eval "$(ssh-agent -s)" `  
   > `# ssh-add ~/.ssh/id_ed25519`
   >
   > Get your public key to add to GitHub:  
   > `# cat ~/.ssh/id_ed25519.pub`  
   > It will be a string of the format '`ssh-ed25519 ... your_email@example.com`'. Copy this string.
   >
   > [Add your SSH key to Github](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account). Under your account menu, select "Settings", then "SSH and GPG Keys". Select "New SSH key" and enter a title. Paste your public key into the key box and click "Add SSH key"

   From your root project directory (ex: mlprojects/), execute the `sparse_checkout.sh` script:  
   >  `# bash mlops-v2/sparse_checkout.sh`  

   This will run the script, using git sparse checkout to build a local copy of your project repository based on your choices configured in the script. It will then create the GitHub repository and push the project code to it.  

   Monitor the script execution for any errors. If there are errors, you can safely remove the local copy of the repository (ex: taxi_fare_regression/) as well as delete the GitHub project repository. After addressing the errors, run the script again.
   
   After the script runs successfully, the GitHub project will be initialized with your project files.

5. **Configure GitHub Actions Secrets**

   This step creates a service principal and GitHub secrets to allow the GitHub action workflows to create and interact with Azure Machine Learning Workspace resources.

      From the command line, execute the following Azure CLI command with your choice of a service principal name:
      > `# az ad sp create-for-rbac --name <service_principal_name> --role contributor --scopes /subscriptions/<subscription_id> --sdk-auth`

      You will get output similar to below:

      >`{`  
      > `"clientId": "<service principal client id>",`  
      > `"clientSecret": "<service principal client secret>",`  
      > `"subscriptionId": "<Azure subscription id>",`  
      > `"tenantId": "<Azure tenant id>",`  
      > `"activeDirectoryEndpointUrl": "https://login.microsoftonline.com",`  
      > `"resourceManagerEndpointUrl": "https://management.azure.com/",`  
      > `"activeDirectoryGraphResourceId": "https://graph.windows.net/",`  
      > `"sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",`  
      > `"galleryEndpointUrl": "https://gallery.azure.com/",`  
      > `"managementEndpointUrl": "https://management.core.windows.net/"`  
      > `}`

      Copy all of this output, braces included.

      From your GitHub project, select **Settings**:

      ![GitHub Settings](./images/gh-settings.png)

      Then select **Secrets**, then **Actions**:

      ![GitHub Secrets](./images/gh-secrets.png)

      Select **New repository secret**. Name this secret **AZURE_CREDENTIALS** and paste the service principal output as the content of the secret.  Select **Add secret**.

      > **Note:**  
      > If deploying the infrastructure using terraform, add the following additional GitHub secrets using the corresponding values from the service principal output as the content of the secret:  
      > 
      > **ARM_CLIENT_ID**  
      > **ARM_CLIENT_SECRET**  
      > **ARM_SUBSCRIPTION_ID**  
      > **ARM_TENANT_ID**  

      The GitHub configuration is complete.

## Deploy Machine Learning Project Infrastructure Using GitHub Actions

1. **Configure Azure ML Environment Parameters**

   In your Github project repository (ex: taxi-fare-regression), there are two configuration files in the root, `config-infra-dev.yml` and `config-infra-prod.yml`. These files are used to define and deploy Dev and Prod Azure Machine Learning environments. With the default deployment, `config-infra-prod.yml` will be used when working with the main branch or your project and `config-infra-dev.yml` will be used when working with any non-main branch.

   It is recommended to first create a dev branch from main and deploy this environment first.

   Edit each file to configure a namespace, postfix string, Azure location, and environment for deploying your Dev and Prod Azure ML environments. Default values and settings in the files are show below:

   > ```bash
   > namespace: mlopsv2 #Note: A namespace with many characters will cause storage account creation to fail due to storage account names having a limit of 24 characters.  
   > postfix: 0001  
   > location: eastus  
   > environment: dev  
   > enable_aml_computecluster: true  
   > enable_monitoring: false  
   >```
   
   The first four values are used to create globally unique names for your Azure environment and contained resources. Edit these values to your liking then save, commit, push, or pr to update these files in the project repository.

   If you are running a Deep Learning workload such as CV or NLP, ensure your subscription and Azure location has available GPU compute. 
   
   > Note:
   >
   > The enable_monitoring flag in these files defaults to False. Enabling this flag will add additional elements to the deployment to support Azure ML monitoring based on https://github.com/microsoft/AzureML-Observability. This will include an ADX cluster and increase the deployment time and cost of the MLOps solution.
   
2. **Deploy Azure Machine Learning Infrastructure**

   In your GitHub project repository (ex: taxi-fare-regression), select **Actions**

   ![GH-actions](./images/gh-actions.png)

   This will display the pre-defined GitHub workflows associated with your project. For a classical machine learning project, the available workflows will look similar to this:

   ![GH-workflows](./images/gh-workflows.png)

   Depending on the the use case, available workflows may vary. Select the workflow to 'deploy-infra'. In this scenario, the workflow to select would be **tf-gha-deploy-infra.yml**. This would deploy the Azure ML infrastructure using GitHub Actions and Terraform.

   ![GH-deploy-infra](./images/gh-deploy-infra.png)

   On the right side of the page, select **Run workflow** and select the branch to run the workflow on. This may deploy Dev Infrastructure if you've created a dev branch or Prod infrastructure if deploying from main. Monitor the pipline for successful completion.

   ![GH-infra-pipeline](./images/gh-infra-pipeline.png)

   When the pipline has complete successfully, you can find your Azure ML Workspace and associated resources by logging in to the Azure Portal.

   Next, a model training and scoring pipelines will be deployed into the new Azure Machine Learning environment.

## Sample Training and Deployment Scenario

The solution accelerator includes code and data for a sample end-to-end machine learning pipeline which runs a linear regression to predict taxi fares in NYC. The pipeline is made up of components, each serving  different functions, which can be registered with the workspace, versioned, and reused with various inputs and outputs. Sample pipelines and workflows for the Computer Vision and NLP scenarios will have different steps and deployment steps.

This training pipeline contains the following steps:

**Prepare Data**  
This component takes multiple taxi datasets (yellow and green) and merges/filters the data, and prepare the train/val and evaluation datasets.  
Input: Local data under ./data/ (multiple .csv files)  
Output: Single prepared dataset (.csv) and train/val/test datasets.

**Train Model**  
This component trains a Linear Regressor with the training set.  
Input: Training dataset  
Output: Trained model (pickle format)  
   
**Evaluate Model**  
   This component uses the trained model to predict taxi fares on the test set.  
   Input: ML model and Test dataset  
   Output: Performance of model and a deploy flag whether to deploy or not.  
   This component compares the performance of the model with all previous deployed models on the new test dataset and decides whether to promote or not model into production. Promoting model into production happens by registering the model in AML workspace.

**Register Model**  
   This component scores the model based on how accurate the predictions are in the test set.  
   Input: Trained model and the deploy flag.  
   Output: Registered model in Azure Machine Learning.  

## Deploying the Model Training Pipeline to the Test Environment

Next, you will deploy the model training pipeline to your new Azure Machine Learning workspace. This pipeline will create a compute cluster instance, register a training environment defining the necessary Docker image and python packages, register a training dataset, then start the training pipeline described in the last section. When the job is complete, the trained model will be registered in the Azure ML workspace and be available for deployment.

In your GitHub project repository (ex: taxi-fare-regression), select **Actions**  
 
   ![GH-actions](./images/gh-actions.png)
      
Select the **deploy-model-training-pipeline** from the workflows listed on the left and the click **Run Workflow** to execute the model training workflow. This will take several minutes to run, depending on the compute size. 

   ![Pipeline Run](./images/gh-training-pipeline.png)
   
   Once completed, a successful run will register the model in the Azure Machine Learning workspace. 

 >**Note**: If you want to check the output of each individual step, for example to view output of a failed run, click a job output, and then click each step in the job to view any output of that step. 

   ![Training Step](./images/gh-training-step.png)

With the trained model registered in the Azure Machine learning workspace, you are ready to deploy the model for scoring.

## Deploying the Trained Model in Dev

This scenario includes prebuilt workflows for two approaches to deploying a trained model, batch scoring or a deploying a model to an endpoint for real-time scoring. You may run either or both of these workflows in your dev branch to test the performance of the model in your Dev Azure ML workspace.

In your GitHub project repository (ex: taxi-fare-regression), select **Actions**  
 
   ![GH-actions](./images/gh-actions.png)

 ### Online Endpoint  
      
Select the **deploy-online-endpoint-pipeline** from the workflows listed on the left and click **Run workflow** to execute the online endpoint deployment pipeline workflow. The steps in this pipeline will create an online endpoint in your Azure Machine Learning workspace, create a deployment of your model to this endpoint, then allocate traffic to the endpoint.

   ![gh online endpoint](./images/gh-online-endpoint.png)
   
   Once completed, you will find the online endpoint deployed in the Azure ML workspace and available for testing.

 ![aml-taxi-oep](./images/aml-taxi-oep.png)

### Batch Endpoint
      
Select the **deploy-batch-endpoint-pipeline** from the workflows and click **Run workflow** to execute the batch endpoint deployment pipeline workflow. The steps in this pipeline will create a new AmlCompute cluster on which to execute batch scoring, create the batch endpoint in your Azure Machine Learning workspace, then create a deployment of your model to this endpoint.

![gh batch endpoint](./images/gh-batch-endpoint.png)

Once completed, you will find the batch endpoint deployed in the Azure ML workspace and available for testing.

![aml-taxi-bep](./images/aml-taxi-bep.png)
   
 
## Moving to Production

Example scenarios can be trained and deployed both for Dev and Prod branches and environments. When you are satisfied with the performance of the model training pipeline, model, and deployment in Testing, Dev pipelines and models can be replicated and deployed in the Production environment.

The sample training and deployment Azure ML pipelines and GitHub workflows can be used as a starting point to adapt your own modeling code and data.


## Next Steps
---

This finishes the demo according to the architectual pattern: Azure Machine Learning Classical Machine Learning. Next you can dive into your Azure Machine Learning service in the Azure Portal and see the inference results of this example model. 

As elements of Azure Machine Learning are still in development, the following components are not part of this demo:
- Model and pipeline promotion from Dev to Prod
- Secure Workspaces
- Model Monitoring for Data/Model Drift
- Automated Retraining
- Model and Infrastructure triggers

Interim it is recommended to schedule the deployment pipeline for development for complete model retraining on a timed trigger.

For questions, please [submit an issue](https://github.com/Azure/mlops-v2/issues) or reach out to the development team at Microsoft.
