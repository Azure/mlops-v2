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

def parse_args():
    parser = argparse.ArgumentParser(description="UCI Credit example")
    parser.add_argument("--data_path", type=str, default='data/', help="Directory path to training data")
    parser.add_argument("--model_path", type=str, default='outputs/', help="Model output directory")
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_args()

    # Make sure model output path exists
    if not os.path.exists(args.model_path):
        os.makedirs(args.model_path)

    print(args.data_path)
    os.listdir(os.getcwd())
    print(os.getcwd())    
        
    # Enable auto logging
    mlflow.sklearn.autolog()
    
    # Read training data
    df = pd.read_csv(os.path.join(args.data_path, 'credit.csv'))
    
    # Train model
    model = model_train(df)

    #copying model to "outputs" directory, this will automatically upload it to Azure ML
    joblib.dump(value=model, filename=os.path.join(args.model_path, 'model.pkl'))

def model_train(df):
    df.drop("Sno", axis=1, inplace=True)

    y_raw = df['Risk']
    X_raw = df.drop('Risk', axis=1)

    categorical_features = X_raw.select_dtypes(include=['object']).columns
    numeric_features = X_raw.select_dtypes(include=['int64', 'float']).columns

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
    encoded_y = le.fit_transform(y_raw)

    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(X_raw, encoded_y, test_size=0.20, stratify=encoded_y, random_state=42)

    # Create sklearn pipeline
    lr_clf = Pipeline(steps=[('preprocessor', feature_engineering_pipeline),
                             ('classifier', LogisticRegression(solver="lbfgs"))])
    # Train the model
    lr_clf.fit(X_train, y_train)

    # Capture metrics
    train_acc = lr_clf.score(X_train, y_train)
    test_acc = lr_clf.score(X_test, y_test)
    print("Training accuracy: %.3f" % train_acc)
    print("Testing accuracy: %.3f" % test_acc)

    return lr_clf

if __name__ == "__main__":
    main()