import argparse
from pathlib import Path
from uuid import uuid4
from datetime import datetime
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle
import mlflow
import mlflow.sklearn

parser = argparse.ArgumentParser("train")
parser.add_argument("--training_data", type=str, help="Path to training data")
parser.add_argument("--model_output", type=str, help="Path of output model")

args = parser.parse_args()

# Enable auto logging
mlflow.sklearn.autolog()

lines = [
    f"Training data path: {args.training_data}",
    f"Model output path: {args.model_output}",
]

for line in lines:
    print(line)

print("mounted_path files: ")
arr = os.listdir(args.training_data)
print(arr)

train_data = pd.read_csv((Path(args.training_data) / "train.csv"))
print(train_data.columns)

# Split the data into input(X) and output(y)
trainy = train_data["cost"]
# X = train_data.drop(['cost'], axis=1)
trainX = train_data[
    [
        "distance",
        "dropoff_latitude",
        "dropoff_longitude",
        "passengers",
        "pickup_latitude",
        "pickup_longitude",
        "store_forward",
        "vendor",
        "pickup_weekday",
        "pickup_month",
        "pickup_monthday",
        "pickup_hour",
        "pickup_minute",
        "pickup_second",
        "dropoff_weekday",
        "dropoff_month",
        "dropoff_monthday",
        "dropoff_hour",
        "dropoff_minute",
        "dropoff_second",
    ]
]

print(trainX.shape)
print(trainX.columns)

# Train a Linear Regression Model with the train set
model = LinearRegression().fit(trainX, trainy)
perf = model.score(trainX, trainy)
print(perf)


# Output the model and test data
pickle.dump(model, open((Path(args.model_output) / "model.sav"), "wb"))