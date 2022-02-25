# Azure MLOps (v2) solution accelerator

_Work in progress_

### MLOps 

MLOps or Machine Learning Ops is a set of practices that aims to automate and operationalise the deployment and maintenance of machine learning models across various stages of the lifecycle of a Data Science process. The purpose of an MLOps process is to drive efficiency, increase repeatability and predictability, enable reuse of code and drive consistency across projects. This enables Data Science teams to deploy Machine Learning models to production reliably and efficiently.  

While MLOps has many overlapping concepts with DevOps and can be seen as a derivation of DevOps, it varies significantly from DevOps due to the nature of Data Science projects. The following Microsoft articles provide a perspective on MLOps from various viewpoints: 

[Cloud Adoption Framework Guidance](https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/ai-machine-learning-mlops) 

[MLOps with Azure Machine Learning](https://docs.microsoft.com/en-us/azure/machine-learning/concept-model-management-and-deployment) 

[MLOps Infographic] 

[MLOps Example Scenario] 

[MLOps for Python models using Azure Machine Learning](https://docs.microsoft.com/en-us/azure/architecture/reference-architectures/ai/mlops-python) 


## Overview of the Accelerator 

The intention of this accelerator is to provide a templatised approach for MLOps in Azure with a recommended architecture. Each organization is unique, and we do not expect that this architecture will suit all organizations, however, this is based on our learning from working with various large and small organizations and can be an excellent starting point for a reference framework which can be used to develop an MLOps framework for the organization.  

With the number of choices available today, it can be difficult for teams to assess all options and make decisions. Various design decisions have been made as part of the development of this accelerator. These decisions provide an opinionated view that reflect most commonly used architectural patterns and practices. By leveraging the tool and capability assessment that has been done as part of the development of this accelerator and only focussing on changes that are needed to meet the specific needs of your organization, you can help your organisation move faster in your journey towards MLOps.   

Following are the key principles that have been applied while building the accelerator: 

  Simplicity 
  
  Segregation of duties 
  
  Reusability 
  
  End to end automation 
  
  Enterprise readiness 

## Repository 

This repo provides a templatised approach for the end-to-end Data Science process and focuses on driving efficiency at each stage. For example, it can take a significant amount of time to bootstrap a new Data Science project, hence the repo provides templates that can be reused to establish a cookie cutter approach for the bootstrapping process to shorten the process from days to hours or minutes. The bootstrapping process encapsulates key MLOps decisions like the various components of the repository, the structure of the repository, the link between model development and model deployment and technology choices for each of the phases of the Data Science process.   

The best way to consume this accelerator will be to choose a complex use case that reflects most of your organisation’s needs from a Data Science perspective and start adjusting this accelerator to accommodate those requirements. The first use case may take longer to deliver, however, once the process has been ironed out, subsequent use cases can be onboarded in a matter of days if not hours.  

The architecture for this accelerator, which has been described in more detail here <insert hyperlink> provides a framework for end-to-end MLOps, from provisioning of resources to the deployment and retraining of models in a production environment. The architecture highlights the key personas that are responsible for each of the stages and lists the key activities that are performed in each phase of a Data Science project. The architecture is based on the concepts of inner, middle and outer loops for a Data Science process which are explained in detail here <insert hyperlink> 


## Getting started
  
This repository hosts the MLOps (v2) solution accelerators. It uses [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/) to generate files and folders based on user selections.

To generate the template files on your local machine, run the following commands:

```bash
pip install cookiecutter
cookiecutter gh:Azure/mlops-v2
```

Then follow the prompts cookiecutter surfaces to generate files ready for your project.

<!-- TODO: Update documentation further -->

You can also use the Azure Portal with the buttons in the list below.

## MLOps infrastructure solution accelerators

| Name                                                    | Description                                          | Try it out      |
| ------------------------------------------------------- | ---------------------------------------------------- | --------------- |
| [default](https://github.com/Azure/mlops-infra-default) | Default Azure Machine Learning infrastructure setup. | [DEPLOY BUTTON] |

### Infrastucture add-ons

| Name                         | Description | Try it out |
| ---------------------------- | ----------- | ---------- |
| [user-with-compute-instance] |             |

## MLOps project solution accelerators

| Name                                                                | Description                                           | Try it out      |
| ------------------------------------------------------------------- | ----------------------------------------------------- | --------------- |
| [classical-ml](https://github.com/Azure/mlops-project-classical-ml) | Classical machine learning solution accelerator demo. | [DEPLOY BUTTON] |

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
