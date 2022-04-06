import os
import sys
import argparse
import joblib
import pandas as pd
import numpy as np

import mlflow
import mlflow.sklearn

from azureml.core import Run

import argparse

run = Run.get_context()
ws = run.experiment.workspace

def parse_args():
    parser = argparse.ArgumentParser(description="UCI Credit example")
    parser.add_argument("--data_path", type=str, default='data/', help="Directory path to training data")
    parser.add_argument("--transformed_data_path", type=str, default='transformed_data/', help="transformed data directory")
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_args()
    transformed_data_path = os.path.join(args.transformed_data_path, run.parent.id)

    # Make sure data output path exists
    if not os.path.exists(transformed_data_path):
        os.makedirs(transformed_data_path)
        
    # Enable auto logging
    mlflow.sklearn.autolog()
    
    # Read training data
    df = pd.read_csv(os.path.join(args.data_path, 'credit.csv'))

    random_data = np.random.rand(len(df))

    msk_train = random_data < 0.7
    msk_val = (random_data >= 0.7) & (random_data < 0.85)
    msk_test = random_data >= 0.85
    
    train = df[msk_train]
    val = df[msk_val]
    test = df[msk_test] 
    
    run.log('TRAIN SIZE', train.shape[0])
    run.log('VAL SIZE', val.shape[0])
    run.log('TEST SIZE', test.shape[0])
    
    run.parent.log('TRAIN SIZE', train.shape[0])
    run.parent.log('VAL SIZE', val.shape[0])
    run.parent.log('TEST SIZE', test.shape[0])
    
    TRAIN_PATH = os.path.join(transformed_data_path, "train.csv")
    VAL_PATH = os.path.join(transformed_data_path, "val.csv")
    TEST_PATH = os.path.join(transformed_data_path, "test.csv")
    
    train.to_csv(TRAIN_PATH, index=False)
    val.to_csv(VAL_PATH, index=False)
    test.to_csv(TEST_PATH, index=False)
    
if __name__ == '__main__':
    main()