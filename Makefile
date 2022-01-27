all:

infra-default:
	git clone https://github.com/Azure/mlops-infra-default
	rm -rf mlops-infra-default/.git
	@echo "Setting up Azure resources and GitHub secret..."
	bash -x mlops-infra-default/setup.sh

project-classical-ml:
	git clone https://github.com/Azure/mlops-project-classical-ml
	rm -rf mlops-project-classical-ml/.git

clean:
	rm -rf infra
	rm -rf project
	mkdir infra
	echo "" > infra/.gitkeep
	mkdir project
	echo "" > project/.gitkeep
