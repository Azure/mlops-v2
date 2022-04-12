import argparse
from pathlib import Path
from uuid import uuid4
from datetime import datetime
import os
import numpy as np
import pandas as pd

from azureml.core import Run, Model
run = Run.get_context()
ws = run.experiment.workspace

parser = argparse.ArgumentParser("prep")
parser.add_argument("--raw_data", type=str, help="Path to raw data")
parser.add_argument("--transformed_data", type=str, help="Path of prepped data")

args = parser.parse_args()

print("hello training world...")

lines = [
    f"Raw data path: {args.raw_data}",
    f"Data output path: {args.transformed_data}",
]

for line in lines:
    print(line)

# ------------ Reading Data ------------ #
# -------------------------------------- #

print("mounted_path files: ")
arr = os.listdir(args.raw_data)
print(arr)

df_list = []
for filename in arr:
    print("reading file: %s ..." % filename)
    with open(os.path.join(args.raw_data, filename), "r") as handle:
        # print (handle.read())
        # ('input_df_%s' % filename) = pd.read_csv((Path(args.training_data) / filename))
        input_df = pd.read_csv((Path(args.raw_data) / filename))
        df_list.append(input_df)


# Prep the green and yellow taxi data
green_data = df_list[0]
yellow_data = df_list[1]

# ------------ Cleanse Data ------------ #
# -------------------------------------- #

# Define useful columns needed

useful_columns = str(
    [
        "cost",
        "distance",
        "dropoff_datetime",
        "dropoff_latitude",
        "dropoff_longitude",
        "passengers",
        "pickup_datetime",
        "pickup_latitude",
        "pickup_longitude",
        "store_forward",
        "vendor",
    ]
).replace(",", ";")
print(useful_columns)

# Rename green taxi columns 
green_columns = str(
    {
        "vendorID": "vendor",
        "lpepPickupDatetime": "pickup_datetime",
        "lpepDropoffDatetime": "dropoff_datetime",
        "storeAndFwdFlag": "store_forward",
        "pickupLongitude": "pickup_longitude",
        "pickupLatitude": "pickup_latitude",
        "dropoffLongitude": "dropoff_longitude",
        "dropoffLatitude": "dropoff_latitude",
        "passengerCount": "passengers",
        "fareAmount": "cost",
        "tripDistance": "distance",
    }
).replace(",", ";")

# Rename yellow taxi columns 
yellow_columns = str(
    {
        "vendorID": "vendor",
        "tpepPickupDateTime": "pickup_datetime",
        "tpepDropoffDateTime": "dropoff_datetime",
        "storeAndFwdFlag": "store_forward",
        "startLon": "pickup_longitude",
        "startLat": "pickup_latitude",
        "endLon": "dropoff_longitude",
        "endLat": "dropoff_latitude",
        "passengerCount": "passengers",
        "fareAmount": "cost",
        "tripDistance": "distance",
    }
).replace(",", ";")

print("green_columns: " + green_columns)
print("yellow_columns: " + yellow_columns)

# Remove null data

def get_dict(dict_str):
    pairs = dict_str.strip("{}").split(";")
    new_dict = {}
    for pair in pairs:
        print(pair)
        key, value = pair.strip().split(":")
        new_dict[key.strip().strip("'")] = value.strip().strip("'")
    return new_dict


def cleanseData(data, columns, useful_columns):
    useful_columns = [
        s.strip().strip("'") for s in useful_columns.strip("[]").split(";")
    ]
    new_columns = get_dict(columns)

    new_df = (data.dropna(how="all").rename(columns=new_columns))[useful_columns]

    new_df.reset_index(inplace=True, drop=True)
    return new_df


green_data_clean = cleanseData(green_data, green_columns, useful_columns)
yellow_data_clean = cleanseData(yellow_data, yellow_columns, useful_columns)

# Append yellow data to green data
combined_df = green_data_clean.append(yellow_data_clean, ignore_index=True)
combined_df.reset_index(inplace=True, drop=True)

output_green = green_data_clean.to_csv((Path(args.transformed_data) / "green_prep_data.csv"))
output_yellow = yellow_data_clean.to_csv((Path(args.transformed_data) / "yellow_prep_data.csv"))
merged_data = combined_df.to_csv((Path(args.transformed_data) / "merged_data.csv"))

# ------------ Filter Data ------------ #
# ------------------------------------- #

# Filter out coordinates for locations that are outside the city border.
combined_df = combined_df.astype(
    {
        "pickup_longitude": "float64",
        "pickup_latitude": "float64",
        "dropoff_longitude": "float64",
        "dropoff_latitude": "float64",
    }
)

latlong_filtered_df = combined_df[
    (combined_df.pickup_longitude <= -73.72)
    & (combined_df.pickup_longitude >= -74.09)
    & (combined_df.pickup_latitude <= 40.88)
    & (combined_df.pickup_latitude >= 40.53)
    & (combined_df.dropoff_longitude <= -73.72)
    & (combined_df.dropoff_longitude >= -74.72)
    & (combined_df.dropoff_latitude <= 40.88)
    & (combined_df.dropoff_latitude >= 40.53)
]

latlong_filtered_df.reset_index(inplace=True, drop=True)

# These functions replace undefined values and rename to use meaningful names.
replaced_stfor_vals_df = latlong_filtered_df.replace(
    {"store_forward": "0"}, {"store_forward": "N"}
).fillna({"store_forward": "N"})

replaced_distance_vals_df = replaced_stfor_vals_df.replace(
    {"distance": ".00"}, {"distance": 0}
).fillna({"distance": 0})

normalized_df = replaced_distance_vals_df.astype({"distance": "float64"})

# Split the pickup and dropoff date further into the day of the week, day of the month, and month values.

temp = pd.DatetimeIndex(normalized_df["pickup_datetime"], dtype="datetime64[ns]")
normalized_df["pickup_date"] = temp.date
normalized_df["pickup_weekday"] = temp.dayofweek
normalized_df["pickup_month"] = temp.month
normalized_df["pickup_monthday"] = temp.day
normalized_df["pickup_time"] = temp.time
normalized_df["pickup_hour"] = temp.hour
normalized_df["pickup_minute"] = temp.minute
normalized_df["pickup_second"] = temp.second

temp = pd.DatetimeIndex(normalized_df["dropoff_datetime"], dtype="datetime64[ns]")
normalized_df["dropoff_date"] = temp.date
normalized_df["dropoff_weekday"] = temp.dayofweek
normalized_df["dropoff_month"] = temp.month
normalized_df["dropoff_monthday"] = temp.day
normalized_df["dropoff_time"] = temp.time
normalized_df["dropoff_hour"] = temp.hour
normalized_df["dropoff_minute"] = temp.minute
normalized_df["dropoff_second"] = temp.second

del normalized_df["pickup_datetime"]
del normalized_df["dropoff_datetime"]

normalized_df.reset_index(inplace=True, drop=True)

print(normalized_df.head)
print(normalized_df.dtypes)

# Drop the pickup_date, dropoff_date, pickup_time, dropoff_time columns because they're
# no longer needed (granular time features like hour,
# minute and second are more useful for model training).
del normalized_df["pickup_date"]
del normalized_df["dropoff_date"]
del normalized_df["pickup_time"]
del normalized_df["dropoff_time"]

# Change the store_forward column to binary values
normalized_df["store_forward"] = np.where((normalized_df.store_forward == "N"), 0, 1)

# Before you package the dataset, run two final filters on the dataset.
# To eliminate incorrectly captured data points,
# filter the dataset on records where both the cost and distance variable values are greater than zero.
final_df = normalized_df[(normalized_df.distance > 0) & (normalized_df.cost > 0)]
final_df.reset_index(inplace=True, drop=True)
print(final_df.head)

# Output data
transformed_data = final_df.to_csv((Path(args.transformed_data) / "transformed_data.csv"))

# Split data into train, val and test datasets

random_data = np.random.rand(len(final_df))

msk_train = random_data < 0.7
msk_val = (random_data >= 0.7) & (random_data < 0.85)
msk_test = random_data >= 0.85

train = final_df[msk_train]
val = final_df[msk_val]
test = final_df[msk_test] 

run.log('train size', train.shape[0])
run.log('val size', val.shape[0])
run.log('test size', test.shape[0])

run.parent.log('train size', train.shape[0])
run.parent.log('val size', val.shape[0])
run.parent.log('test size', test.shape[0])

train_data = train.to_csv((Path(args.transformed_data) / "train.csv"))
val_data = val.to_csv((Path(args.transformed_data) / "val.csv"))
test_data = test.to_csv((Path(args.transformed_data) / "test.csv"))

