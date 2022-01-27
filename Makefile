all:

infra-default:
	git clone https://github.com/Azure/mlops-infra-default
	rm -r mlops-infra-default/.git
	@echo "Setting up Azure resources and GitHub secret..."
	bash -x mlops-infra-default/setup.sh

project-classical-ml:
	git clone https://github.com/Azure/mlops-project-classical-ml
	rm -r mlops-project-classical-ml/.git

clean:
	rm -r infra
	rm -r project
	mkdir infra
	echo "" > infra/.gitkeep
	mkdir project
	echo "" > project/.gitkeep
