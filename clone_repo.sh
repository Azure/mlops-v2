#!/bin/bash

remove_submodule() {
        mv $1 $1_tmp
        git submodule deinit $1
        git rm -r --cached $1
        mv $1_tmp $1
        git add $1
        git commit -m "Removed SubModule "+ $1
}

check_git(){
        if git --version 2>&1 >/dev/null ; then
                echo "Git is installed. Skipping installation"
        else
                echo "Git is not installed. Installing.."
                sudo apt install git
        fi
}

check_git

#Clone the MLOps Repository
git clone https://github.com/Azure/mlops-v2.git --recurse-submodules
cd mlops-v2/

#Remove the submodules
remove_submodule infrastructure
remove_submodule data-science-regression

#Disconnect the main repo
git remote rm origin
