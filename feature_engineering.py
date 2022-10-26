import json

import pandas as pd
import os

from numpy import mean

path = r"C:\Users\samuello\Downloads\III\旺欉\code\input-data\label data"
files = os.listdir(path)

lst = []
cols = ["ingot_max", "ingot_min", "ingot_len", "ingot_maxmin_diff",
        "oil_pressure_max", "oil_pressure_len",
        "mould_mean", "mould_maxmin_diff", "bucket_mean", "bucket_maxmin_diff",
        "label"]
data = pd.DataFrame()

for file in files:  # 8 input csv files
    df = pd.read_csv(os.path.join(path, file))
    for i in range(len(df)):  # length of every column

        # type: list
        ingot_data = json.loads(df["ingot"].iloc[i])
        oil_pressure_data = json.loads(df["oil_pressure"].iloc[i])
        mould_data = json.loads(df["mould"].iloc[i])
        bucket_data = json.loads(df["bucket"].iloc[i])

        lst = [
            max(ingot_data), min(ingot_data), len(ingot_data), max(ingot_data) - min(ingot_data),
            max(oil_pressure_data), len(oil_pressure_data),
            mean(mould_data), max(mould_data) - min(mould_data),
            mean(bucket_data), max(bucket_data) - min(bucket_data),
            df["label"].iloc[i]
        ]
        data = pd.concat([data, pd.DataFrame(lst).T])

data.columns = cols
data = data.reset_index(drop=True)
data.to_csv("./input-data/input.csv", index=False)
