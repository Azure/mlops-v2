# Azure MLOps (v2) solution accelerator

_Work in progress_

### Microsoft's State of MLOps 

MLOps or Machine Learning Ops is a set of practices that aims to automate and operationalise the deployment and maintenance of machine learning models across various stages of the lifecycle of a Data Science process. The purpose of an MLOps process is to drive efficiency, increase repeatability and predictability, enable reuse of code and drive consistency across projects. This enables Data Science teams to deploy Machine Learning models to production reliably and efficiently.  

While MLOps has many overlapping concepts with DevOps and can be seen as a derivation of DevOps, it varies significantly from DevOps due to the nature of Data Science projects. The following Microsoft articles provide a perspective on MLOps from various viewpoints: 

[Cloud Adoption Framework Guidance](https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/ai-machine-learning-mlops) 

[MLOps with Azure Machine Learning](https://docs.microsoft.com/en-us/azure/machine-learning/concept-model-management-and-deployment) 

[MLOps Infographic] 

[MLOps Example Scenario] 

[MLOps for Python models using Azure Machine Learning](https://docs.microsoft.com/en-us/azure/architecture/reference-architectures/ai/mlops-python) 


## Overview of the MLOps Solution Accelerator 

The accelerator provides a modular end-to-end approach for MLOps in Azure based on pattern architectures. As each organization is unique, we do not expect that each pattern architecture will suit all organizations, however, Digital Natives or enterprises will be able to deploy an MLOps ecosystem fast, simple, reliable, modular, and secure. The time to product is measurable shorter under incerased scalability.

Following are the key principles that have been applied while building the accelerator: 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Simplicity 
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Segregation of duties 
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Reusability 
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Modularity
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Enterprise readiness 


## Repository 

This repo provides a templatised approach for the end-to-end Data Science process and focuses on driving efficiency at each stage. For example, it can take a significant amount of time to bootstrap a new Data Science project, hence the repo provides templates that can be reused to establish a cookie cutter approach for the bootstrapping process to shorten the process from days to hours or minutes. The bootstrapping process encapsulates key MLOps decisions like the various components of the repository, the structure of the repository, the link between model development and model deployment and technology choices for each of the phases of the Data Science process.   

The best way to consume this accelerator will be to choose a complex use case that reflects most of your organisation’s needs from a Data Science perspective and start adjusting this accelerator to accommodate those requirements. The first use case may take longer to deliver, however, once the process has been ironed out, subsequent use cases can be onboarded in a matter of days if not hours.  

The architecture for this accelerator, which has been described in more detail here <insert hyperlink> provides a framework for end-to-end MLOps, from provisioning of resources to the deployment and retraining of models in a production environment. The architecture highlights the key personas that are responsible for each of the stages and lists the key activities that are performed in each phase of a Data Science project. The architecture is based on the concepts of inner, middle and outer loops for a Data Science process which are explained in detail here <insert hyperlink> 


## Getting started with AML Classical ML Demo
  
The demo follows the Classical Machine Learning Pattern with Azure Machine Learning.
  
![AML CML](/documentation/architecturepattern/AzureML_CML_Architecture_v0.7.jpg)
  
Please follow the instructions to execute the demo accordingly:
  
&nbsp;&nbsp;1.
&nbsp;&nbsp;2.
&nbsp;&nbsp;3.
&nbsp;&nbsp;...

Following the demo helps to understand the concept of the solution accelerator, architectual pattern, and ongoing work extending the solution accelerator to other patterns. Feel free to replace the inner loop model with your model and rerun accordingly.

  
## (Coming Soon) One-click Deployments:
  
## MLOps infrastructure deployment

| Name                                                    | Description                                          | Try it out      |
| ------------------------------------------------------- | ---------------------------------------------------- | --------------- |
| [default](https://github.com/Azure/mlops-infra-default) | Default Azure Machine Learning infrastructure setup. | [DEPLOY BUTTON] |

## MLOps use case deployment

| Name                                                                | AI Workload Type                   | Services                                 | Try it out      |
|-------------------------------------------------------------------- | -----------------------------------| ---------------------------------------- | --------------- |
| [classical-ml](https://github.com/Azure/mlops-project-classical-ml) | Classical machine learning         | Azure Machine Learning                   | [DEPLOY BUTTON] |
|                                                                     | Computer Vision                    | Azure Machine Learning                   | [DEPLOY BUTTON] |
|                                                                     | Natural Language Processing        | Azure Machine Learning                   | [DEPLOY BUTTON] |
|                                                                     | Classical machine learning         | Azure Machine Learning, Azure Databricks | [DEPLOY BUTTON] |
|                                                                     | Computer Vision                    | Azure Machine Learning, Azure Databricks | [DEPLOY BUTTON] |
|                                                                     | Natural Language Processing        | Azure Machine Learning, Azure Databricks | [DEPLOY BUTTON] |
|                                                                     | Classical machine learning with R  | Azure Machine Learning                   | [DEPLOY BUTTON] |  
|                                                                     | Edge AI                            | Azure Machine Learning                   | [DEPLOY BUTTON] |  


## Contributing

TBD. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.


## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
  
 
## Reference

- links to documentation here (and in sidebar)
