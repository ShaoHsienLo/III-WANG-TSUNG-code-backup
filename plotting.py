import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


df = pd.read_csv("./unlabeled-data/format-data(per second)/Oct-5-data.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%Y-%m-%d %H:%M:%S")
df = df[df["Timestamp"] > datetime(2022, 10, 5, 11, 44, 0)]
print(df.index[0])
