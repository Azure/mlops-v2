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
from sklearn import metrics

from fairlearn.metrics._group_metric_set import _create_group_metric_set
from azureml.contrib.fairness import upload_dashboard_dictionary, download_dashboard_by_upload_id

from interpret_community import TabularExplainer
from azureml.interpret import ExplanationClient

from azureml.core import Run, Model
run = Run.get_context()
ws = run.experiment.workspace

def parse_args():
    parser = argparse.ArgumentParser(description="UCI Credit example")
    parser.add_argument("--transformed_data_path", type=str, default='transformed_data/', help="Directory path to training data")
    parser.add_argument('--model_name', type=str, help='Name under which model is registered')
    parser.add_argument("--model_path", type=str, default='trained_model/', help="Model output directory")
    parser.add_argument("--explainer_path", type=str, default='trained_model/', help="Model output directory")
    parser.add_argument("--evaluation_path", type=str, default='evaluation_results/', help="Evaluation results output directory")
    parser.add_argument('--deploy_flag', type=str, help='A deploy flag whether to deploy or no')
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_args()
    transformed_data_path = os.path.join(args.transformed_data_path, run.parent.id)
    model_path = os.path.join(args.model_path, run.parent.id)
    explainer_path = os.path.join(args.explainer_path, run.parent.id)
    evaluation_path = os.path.join(args.evaluation_path, run.parent.id)

    # Make sure evaluation output path exists
    if not os.path.exists(evaluation_path):
        os.makedirs(evaluation_path)
        
    # Make sure explainer output path exists
    if not os.path.exists(explainer_path):
        os.makedirs(explainer_path)

    # Enable auto logging
    mlflow.sklearn.autolog()
    
    # Read training & testing data
    print(os.path.join(transformed_data_path, 'train.csv'))
    train = pd.read_csv(os.path.join(transformed_data_path, 'train.csv'))
    train.drop("Sno", axis=1, inplace=True)
    y_train = train['Risk']
    X_train = train.drop('Risk', axis=1)
    
    test = pd.read_csv(os.path.join(transformed_data_path, 'test.csv'))
    test.drop("Sno", axis=1, inplace=True)
    y_test = test['Risk']
    X_test = test.drop('Risk', axis=1)
    
    run.log('TEST SIZE', test.shape[0])
    
    # Load model
    model = joblib.load(os.path.join(model_path, 'model.pkl'))

    # ---------------- Model Evaluation ---------------- #
    # Evaluate model using testing set
    
    # Capture Accuracy Score
    test_acc = model.score(X_test, y_test)

    # Capture ML Metrics
    test_metrics = {
        "Test Accuracy": metrics.accuracy_score(y_test, model.predict(X_test)),
        "Test Recall": metrics.recall_score(y_test, model.predict(X_test), pos_label="good"),
        "Test Precison": metrics.precision_score(y_test, model.predict(X_test), pos_label="good"),
        "Test F1 Score": metrics.f1_score(y_test, model.predict(X_test), pos_label="good")
    }

    # Capture Confusion Matrix
    test_cm = metrics.plot_confusion_matrix(model, X_test, y_test)

    # Save and test eval metrics
    print("Testing accuracy: %.3f" % test_acc)
    run.log('Testing accuracy', test_acc)
    run.parent.log('Testing accuracy', test_acc)
    with open(os.path.join(evaluation_path, "metrics.json"), 'w+') as f:
        json.dump(test_metrics, f)
    test_cm.figure_.savefig(os.path.join(evaluation_path, "confusion_matrix.jpg"))
    test_cm.figure_.savefig("confusion_matrix.jpg")
    run.log_image(name='Confusion Matrix Test Dataset', path="confusion_matrix.jpg")
    run.parent.log_image(name='Confusion Matrix Test Dataset', path="confusion_matrix.jpg")

    
    # -------------------- Promotion ------------------- #
    test_accuracies = {}
    test_predictions = {}
    labels_dict = {"good": int(1), "bad": int(0)}
    y_test_labels = [labels_dict[x] for x in y_test]
    
    for model_run in Model.list(ws):
        if model_run.name == args.model_name:
            mdl_path = Model.download(model_run, exist_ok=True)
            mdl = joblib.load(os.path.join(mdl_path, 'model.pkl'))
            
            test_accuracies[model_run.id] = mdl.score(X_test, y_test)
            test_predictions[model_run.id] = [labels_dict[x] for x in mdl.predict(X_test)]
     
    if test_accuracies:
        if test_acc >= max(list(test_accuracies.values())):
            deploy_flag = 1
        else:
            deploy_flag = 0
    else:
        deploy_flag = 1
            
    with open(args.deploy_flag, 'w') as f:
        f.write('%d' % int(deploy_flag))
        
    run.log('deploy flag', bool(deploy_flag))
    run.parent.log('deploy flag', bool(deploy_flag))
        
    test_accuracies["current model"] = test_acc
    model_runs_metrics_plot = pd.DataFrame(test_accuracies, index=["accuracy"]).plot(kind='bar', figsize=(15, 10))
    model_runs_metrics_plot.figure.savefig(os.path.join(evaluation_path, "model_runs_metrics_plot.png"))    
    model_runs_metrics_plot.figure.savefig("model_runs_metrics_plot.png")    
    run.log_image(name='MODEL RUNS METRICS COMPARISON', path="model_runs_metrics_plot.png")
    run.parent.log_image(name='MODEL RUNS METRICS COMPARISON', path="model_runs_metrics_plot.png")

    # -------------------- FAIRNESS ------------------- #
    # Calculate Fairness Metrics over Sensitive Features
    # Create a dictionary of model(s) you want to assess for fairness 
    
    sensitive_features = ["Sex"]
    sf = { col: X_test[[col]] for col in sensitive_features }
    test_predictions["currrent model"] = [labels_dict[x] for x in model.predict(X_test)]
    
    dash_dict_all = _create_group_metric_set(y_true=y_test_labels,
                                             predictions=test_predictions,
                                             sensitive_features=sf,
                                             prediction_type='binary_classification',
                                            )
    
    # Upload the dashboard to Azure Machine Learning
    dashboard_title = "Fairness insights Comparison of Models"
    # Set validate_model_ids parameter of upload_dashboard_dictionary to False if you have not registered your model(s)
    upload_id = upload_dashboard_dictionary(run,
                                            dash_dict_all,
                                            dashboard_name=dashboard_title,
                                            validate_model_ids=False)
    print("\nUploaded to id: {0}\n".format(upload_id))

    upload_id_pipeline = upload_dashboard_dictionary(run.parent,
                                            dash_dict_all,
                                            dashboard_name=dashboard_title,
                                            validate_model_ids=False)
    print("\nUploaded to id: {0}\n".format(upload_id_pipeline))
    
    
    # -------------------- Explainability ------------------- #
    tabular_explainer = TabularExplainer(model.steps[-1][1],
                                     initialization_examples=X_train,
                                     features=X_train.columns,
                                     classes=[0, 1],
                                     transformations=model.steps[0][1])
                                     
    joblib.dump(tabular_explainer, os.path.join(explainer_path, "explainer"))

    # you can use the training data or the test data here, but test data would allow you to use Explanation Exploration
    global_explanation = tabular_explainer.explain_global(X_test)

    # if the PFIExplainer in the previous step, use the next line of code instead
    # global_explanation = explainer.explain_global(x_train, true_labels=y_train)

    # sorted feature importance values and feature names
    sorted_global_importance_values = global_explanation.get_ranked_global_values()
    sorted_global_importance_names = global_explanation.get_ranked_global_names()

    print("Explainability feature importance:")
    # alternatively, you can print out a dictionary that holds the top K feature names and values
    global_explanation.get_feature_importance_dict()
    
    client = ExplanationClient.from_run(run)
    client.upload_model_explanation(global_explanation, comment='global explanation: all features')

    # upload dashboard to parent run
    client_parent = ExplanationClient.from_run(run.parent)
    client_parent.upload_model_explanation(global_explanation, comment='global explanation: all features')
    

if __name__ == "__main__":
    main()
