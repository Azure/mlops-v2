  
import os
import glob
import json
import argparse
import numpy as np
import pandas as pd
import joblib

from azureml.core.model import Model

model = None
explainer = None

def init():
    global model, explainer
    print("Started batch scoring by running init()")
    
    model_path = os.path.join(os.environ["AZUREML_MODEL_DIR"], "model.sav")

    print(f"Model path: {model_path}")
    model = joblib.load(model_path)

def run(file_list):
    
    print(f"Files to process: {file_list}")
    results = pd.DataFrame(columns=["Sno", "ProbaGoodCredit", "ProbaBadCredit", "FeatureImportance"])
    
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