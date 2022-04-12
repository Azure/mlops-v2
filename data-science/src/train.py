import os
import sys
import argparse
import joblib
import pandas as pd

import mlflow
import mlflow.sklearn

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

from azureml.core import Run
run = Run.get_context()
ws = run.experiment.workspace

def parse_args():
    parser = argparse.ArgumentParser(description="UCI Credit example")
    parser.add_argument("--transformed_data_path", type=str, default='transformed_data/', help="Directory path to training data")
    parser.add_argument("--model_path", type=str, default='trained_model/', help="Model output directory")
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_args()

    transformed_data_path = os.path.join(args.transformed_data_path, run.parent.id)
    model_path = os.path.join(args.model_path, run.parent.id)

    # Make sure model output path exists
    if not os.path.exists(model_path):
        os.makedirs(model_path)

    # Enable auto logging
    mlflow.sklearn.autolog()
    
    # Read training data
    print(os.path.join(transformed_data_path, 'train.csv'))
    train = pd.read_csv(os.path.join(transformed_data_path, 'train.csv'))
    val = pd.read_csv(os.path.join(transformed_data_path, 'val.csv'))
    
    run.log('TRAIN SIZE', train.shape[0])
    run.log('VAL SIZE', val.shape[0])
    
    # Train model
    model = model_train(train, val)

    #copying model to "outputs" directory, this will automatically upload it to Azure ML
    joblib.dump(value=model, filename=os.path.join(model_path, 'model.pkl'))

def model_train(train, val):
    
    train.drop("Sno", axis=1, inplace=True)
    val.drop("Sno", axis=1, inplace=True)

    y_train = train['Risk']
    X_train = train.drop('Risk', axis=1)

    y_val = val['Risk']
    X_val = val.drop('Risk', axis=1)
    
    categorical_features = X_train.select_dtypes(include=['object']).columns
    numeric_features = X_train.select_dtypes(include=['int64', 'float']).columns

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value="missing")),
        ('onehotencoder', OneHotEncoder(categories='auto', sparse=False))])

    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())])

    feature_engineering_pipeline = ColumnTransformer(
        transformers=[
            ('numeric', numeric_transformer, numeric_features),
            ('categorical', categorical_transformer, categorical_features)
        ], remainder="drop")

    # Encode Labels
    le = LabelEncoder()
    encoded_y = le.fit_transform(y_train)

    # Create sklearn pipeline
    lr_clf = Pipeline(steps=[('preprocessor', feature_engineering_pipeline),
                             ('classifier', LogisticRegression(solver="lbfgs"))])
    # Train the model
    lr_clf.fit(X_train, y_train)

    # Capture metrics
    train_acc = lr_clf.score(X_train, y_train)
    val_acc = lr_clf.score(X_val, y_val)
    print("Training accuracy: %.3f" % train_acc)
    print("Validation accuracy: %.3f" % val_acc)

    run.log('Training accuracy', train_acc)
    run.log('Validation accuracy', val_acc)

    return lr_clf

if __name__ == "__main__":
    main()