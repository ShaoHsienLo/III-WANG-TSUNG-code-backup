from pandas_profiling import ProfileReport
import sweetviz as sv
import pandas as pd

pd.set_option("display.max_columns", 100)

df_1_2 = pd.read_csv("./labeled-data/1st-2st-labeling/all-labeled-data.csv")
df_3 = pd.read_csv("./labeled-data/3st-labeling/all-labeled-data.csv")
data = pd.concat([df_1_2, df_3], ignore_index=True)
data = data.drop(columns=["original label"])

# Pandas Profiling
report = ProfileReport(data, title="Pandas Profiling", minimal=True)
report.to_file("./eda/400多錠的/Pandas-Profiling.html")

# Sweetviz
# report = sv.analyze(data)
# report.show_html(filepath='./eda/撈取資料範圍1.0到1.6的/Sweetviz-Profiling.html', open_browser=False)

