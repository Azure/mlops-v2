import argparse
import pandas as pd
import os
from pathlib import Path
from sklearn.linear_model import LinearRegression
import pickle
from sklearn.metrics import mean_squared_error, r2_score
from azureml.core import Run, Experiment, Model

# current run 
run = Run.get_context()
ws = run.experiment.workspace

parser = argparse.ArgumentParser("predict")
parser.add_argument("--model_name", type=str, help="Name of registered model")
parser.add_argument("--model_input", type=str, help="Path of input model")
parser.add_argument("--test_data", type=str, help="Path to test data")
parser.add_argument("--predictions", type=str, help="Path of predictions")
parser.add_argument("--score_report", type=str, help="Path to score report")
parser.add_argument('--deploy_flag', type=str, help='A deploy flag whether to deploy or no')

# ---------------- Model Evaluation ---------------- #

args = parser.parse_args()

lines = [
    f"Model path: {args.model_input}",
    f"Test data path: {args.test_data}",
    f"Predictions path: {args.predictions}",
    f"Scoring output path: {args.score_report}",
]

for line in lines:
    print(line)

# Load the test data

print("mounted_path files: ")
arr = os.listdir(args.test_data)

print(arr)

test_data = pd.read_csv((Path(args.test_data) / "test.csv"))
print(test_data.columns)

testy = test_data["cost"]
# testX = test_data.drop(['cost'], axis=1)
testX = test_data[
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
print(testX.shape)
print(testX.columns)

# Load the model from input port
model = pickle.load(open((Path(args.model_input) / "model.sav"), "rb"))
# model = (Path(args.model_input) / 'model.txt').read_text()
# print('Model: ', model)

# Compare predictions to actuals (testy)
output_data = testX.copy()
output_data["actual_cost"] = testy
output_data["predicted_cost"] = model.predict(testX)

# Save the output data with feature columns, predicted cost, and actual cost in csv file
output_data.to_csv((Path(args.predictions) / "predictions.csv"))

# Print the results of scoring the predictions against actual values in the test data
# The coefficients
print("Coefficients: \n", model.coef_)

actuals = output_data["actual_cost"]
predictions = output_data["predicted_cost"]

# The mean squared error
print("Mean squared error: %.2f" % mean_squared_error(actuals, predictions))
# The coefficient of determination: 1 is perfect prediction
print("Coefficient of determination: %.2f" % r2_score(actuals, predictions))
print("Model: ", model)

# Print score report to a text file
(Path(args.score_report) / "score.txt").write_text(
    "Scored with the following model:\n{}".format(model)
)
with open((Path(args.score_report) / "score.txt"), "a") as f:
    f.write("\n Coefficients: \n %s \n" % str(model.coef_))
    f.write("Mean squared error: %.2f \n" % mean_squared_error(actuals, predictions))
    f.write("Coefficient of determination: %.2f \n" % r2_score(actuals, predictions))

# -------------------- Promotion ------------------- #
test_scores = {}
test_predictions = {}
test_score = r2_score(actuals, predictions) # current model
for model_run in Model.list(ws):
    if model_run.name == args.model_name:
        model_path = Model.download(model_run, exist_ok=True)
        mdl = pickle.load(open((Path(model_path)), "rb"))
        test_predictions[model_run.id] = mdl.predict(testX)
        test_scores[model_run.id] = r2_score(actuals, test_predictions[model_run.id])
    
print(test_scores)
if test_scores:
    if test_score >= max(list(test_scores.values())):
        deploy_flag = 1
    else:
        deploy_flag = 0
else:
    deploy_flag = 1

with open((Path(args.deploy_flag) / "deploy_flag"), 'w') as f:
    f.write('%d' % int(deploy_flag))
    
run.log('deploy flag', bool(deploy_flag))
run.parent.log('deploy flag', bool(deploy_flag))
    
test_scores["current model"] = test_score
model_runs_metrics_plot = pd.DataFrame(test_scores, index=["r2 score"]).plot(kind='bar', figsize=(15, 10))
model_runs_metrics_plot.figure.savefig("model_runs_metrics_plot.png")
model_runs_metrics_plot.figure.savefig(Path(args.score_report) / "model_runs_metrics_plot.png")
run.log_image(name='MODEL RUNS METRICS COMPARISON', path="model_runs_metrics_plot.png")
run.parent.log_image(name='MODEL RUNS METRICS COMPARISON', path="model_runs_metrics_plot.png")

