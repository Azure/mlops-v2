# Azure MLOps (v2) solution accelerator

![Header](documentation/repositoryfiles/mlopsheader.jpg)

Welcome to the MLOps (v2) solution accelerator repository! This project is intended to serve as *the* starting point for MLOps implementation in Azure.

MLOps is a set of repeatable, automated, and collaborative workflows with best practices that empower teams of ML professionals to quickly and easily get their machine learning models deployed into production. You can learn more about MLOps here:

- [MLOps with Azure Machine Learning](https://azure.microsoft.com/services/machine-learning/mlops/#features)
- [Cloud Adoption Framework Guidance](https://docs.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/ai-machine-learning-mlops)
- [How: Machine Learning Operations](https://docs.microsoft.com/azure/machine-learning/concept-model-management-and-deployment)

## Prerequisites

1. An Azure subscription. If you don't have an Azure subscription, [create a free account](https://aka.ms/AzureMLFree) before you begin.
2. The [Terraform extension for Azure DevOps](https://marketplace.visualstudio.com/items?itemName=ms-devlabs.custom-terraform-tasks) if you are using Terraform to spin up infrastructure
3. Git bash, WSL or another shell script editor on your local machine

## Project overview

The solution accelerator provides a modular end-to-end approach for MLOps in Azure based on pattern architectures. As each organization is unique, solutions will often need to be customized to fit the organization's needs.

The solution accelerator goals are:

- Simplicity
- Modularity
- Repeatability & Security
- Collaboration
- Enterprise readiness

It accomplishes these goals with a template-based approach for end-to-end data science, driving operational efficiency at each stage. You should be able to get up and running with the solution accelerator in a few hours.

## 👤 Getting started: Azure Machine Learning Pattern Demo
  
The demo follows the classical machine learning or computer vision pattern with Azure Machine Learning.

Azure Machine Learning - Classical Machine Learning Architecture:
![AzureML CML](/documentation/architecturepattern/AzureML_CML_Architecture.png)

Azure Machine Learning - Computer Vision Architecture:
![AzureML CV](/documentation/architecturepattern/AzureML_SupervisedCV_Architecture.png)
  
‼️ **Please follow the instructions to execute the demo accordingly: [Quickstart](https://github.com/Azure/mlops-v2/blob/main/QUICKSTART.md)** ‼️

‼️ **Please submit any issues here: [Issues](https://github.com/Azure/mlops-v2/issues)** ‼️

## 📐 Pattern Architectures: Key concepts

| Link                                                    | AI Pattern                                                              |
| ------------------------------------------------------- | ----------------------------------------------------------------------- |
| [Pattern AzureML CML](https://github.com/Azure/mlops-v2/blob/main/documentation/architecturepattern/AzureML_CML_Architecture.png) | Azure Machine Learning - Classical Machine Learning                     |
| [Pattern AzureML CV](https://github.com/Azure/mlops-v2/blob/main/documentation/architecturepattern/AzureML_SupervisedCV_Architecture.png)                                                 | Azure Machine Learning - Computer Vision                                |
| [Pattern AzureML NLP](https://github.com/Azure/mlops-v2/blob/main/documentation/architecturepattern/AzureML_NLP_Classification_Architecture.png)                                                 | Azure Machine Learning - Natural Language Processing                    |
| [TBD]                                                   | Azure Machine Learning / Azure Databricks - Classical Machine Learning  |
| [TBD]                                                   | Azure Machine Learning / Azure Databricks - Computer Vision             |
| [TBD]                                                   | Azure Machine Learning / Azure Databricks - Natural Language Processing |
| [TBD]                                                   | Azure Machine Learning - Edge AI                                        |

## 📯 (Coming Soon) One-click deployments
  
## 📯 MLOps infrastructure deployment

| Name                                                         | Description                                                | Try it out      |
| ------------------------------------------------------------ | ---------------------------------------------------------- | --------------- |
| [Outer Loop](https://github.com/Azure/mlops-templates)       | Default Azure Machine Learning outer infrastructure setup  | [DEPLOY BUTTON] |
| [TBD]                                                        | Default Responsible AI for Classical Machine Learning      | [DEPLOY BUTTON] |
| [Feature Store FEAST](https://github.com/Azure/feast-azure)  | Default Feature Store using FEAST                          | [DEPLOY BUTTON] |
| [Feature Store Feathr](https://github.com/linkedin/feathr)   | Feature Store Pattern using Feathr                         | [DEPLOY BUTTON] |

## 📯 MLOps use case deployment

| Name                                                                | AI Workload Type                   | Services                                 | Try it out      |
|-------------------------------------------------------------------- | -----------------------------------| ---------------------------------------- | --------------- |
| [classical-ml](https://github.com/Azure/mlops-project-template/tree/main/classical)     | Classical machine learning         | Azure Machine Learning                   | [DEPLOY BUTTON] |
| [CV](https://github.com/Azure/mlops-project-template/tree/main/cv)  | Computer Vision                    | Azure Machine Learning                   | [DEPLOY BUTTON] |
| [TBD]                                                               | Natural Language Processing        | Azure Machine Learning                   | [DEPLOY BUTTON] |
| [TBD]                                                               | Classical machine learning         | Azure Machine Learning, Azure Databricks | [DEPLOY BUTTON] |
| [TBD]                                                               | Computer Vision                    | Azure Machine Learning, Azure Databricks | [DEPLOY BUTTON] |
| [TBD]                                                               | Natural Language Processing        | Azure Machine Learning, Azure Databricks | [DEPLOY BUTTON] |
| [TBD]                                                               | Edge AI                            | Azure Machine Learning                   | [DEPLOY BUTTON] |  

## Contributing

This project welcomes contributions and suggestions. To learn more visit the contributing section, see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
