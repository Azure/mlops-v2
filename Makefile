all:

infra-default:
	rm -rf infra
	git clone https://github.com/Azure/mlops-infra-default infra
	rm -rf infra/.git
	@echo "Setting up Azure resources and GitHub secret..."
	bash -x infra/setup.sh

project-classical-ml:
	rm -rf project
	git clone https://github.com/Azure/mlops-project-classical-ml project
	rm -rf project/.git

clean:
	rm -rf infra
	rm -rf project
	mkdir infra
	echo "" > infra/.gitkeep
	mkdir project
	echo "" > project/.gitkeep

clean-infra:
	bash -x infra/cleanup.sh