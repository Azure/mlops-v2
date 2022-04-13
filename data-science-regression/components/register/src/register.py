# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import argparse
from pathlib import Path
from azureml.core import Run, Experiment, Model

parser = argparse.ArgumentParser()
parser.add_argument('--model_name', type=str, help='Name under which model will be registered')
parser.add_argument('--model_path', type=str, help='Model directory')
parser.add_argument('--deploy_flag', type=str, help='A deploy flag whether to deploy or no')
args, _ = parser.parse_known_args()

print(f'Arguments: {args}')
model_name = args.model_name
model_path = args.model_path

with open((Path(args.deploy_flag) / "deploy_flag"), 'r') as f:
    deploy_flag = int(f.read())
        
# current run is the registration step
run = Run.get_context()
ws = run.experiment.workspace

if deploy_flag==1:
    print("Registering ", args.model_name)
    registered_model = Model.register(model_path=args.model_path,
                                      model_name=args.model_name,
                                      workspace=ws)
    print("Registered ", registered_model.id)
else:
    print("Model will not be registered!")