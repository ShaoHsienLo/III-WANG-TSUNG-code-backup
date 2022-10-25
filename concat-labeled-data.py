import pandas as pd
import os

df_0905 = pd.read_csv("./labeled-data/3st-labeling/Sep-5-labeled-data.csv")
df_0908 = pd.read_csv("./labeled-data/3st-labeling/Sep-8-labeled-data.csv")
df_0922 = pd.read_csv("./labeled-data/3st-labeling/Sep-22-labeled-data.csv")
df_1007 = pd.read_csv("./labeled-data/3st-labeling/Oct-7-labeled-data.csv")

df = pd.concat([df_0905, df_0908])
df = pd.concat([df, df_0922])
df = pd.concat([df, df_1007])
df.to_csv("./labeled-data/3st-labeling/no-Oct-5-labeled-data.csv", index=False)

# path = r"C:\Users\samuello\Downloads\III\旺欉\code\labeled-data\3st-labeling"
# files = os.listdir(path)
# data = pd.DataFrame()
# length = 0
#
# for file in files:
#     print(file)
#
#     df = pd.read_csv(os.path.join(path, file))
#     length = length + len(df)
#     if not data.empty:
#         data = pd.concat([data, df])
#     else:
#         data = df
#
# print(data.head())
# print(data.shape)
# print(length)
#
# data.to_csv(os.path.join(path, "all-labeled-data.csv"), index=False)


