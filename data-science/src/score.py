  
import os
import glob
import json
import argparse
import numpy as np
import pandas as pd
import joblib
from azureml.core.model import Model

model = None

def init():
    global model
    print("Started batch scoring by running init()")
    
    parser = argparse.ArgumentParser('batch_scoring')
    parser.add_argument('--model_name', type=str, help='Model to use for batch scoring')
    args, _ = parser.parse_known_args()
    
    model_path = Model.get_model_path(args.model_name)
    print(f"Model path: {model_path}")
    model = joblib.load(model_path)

def run(file_list):
    print(f"Files to process: {file_list}")
    results = pd.DataFrame(columns=["Sno", "ProbaGoodCredit", "ProbaBadCredit"])
    for filename in file_list:
        df = pd.read_csv(filename)
        sno = df["Sno"]
        df = df.drop("Sno", axis=1)
        proba = model.predict_proba(df)
        proba = pd.DataFrame(data=proba, columns=["ProbaGoodCredit", "ProbaBadCredit"])
        result = pd.concat([sno, proba], axis=1)
        results = results.append(result)
        print(f"Batch scored: {filename}")
    return results