import numpy as np
import pandas as pd
import os
from statistics import mode
from scipy.stats import iqr, sem
from lime import lime_tabular
import joblib


def _ptp(x):
    return np.ptp(x.values)


def _iqr(x):
    return iqr(x.values)


def _sem(x):
    return sem(x.values)


X_train = pd.read_csv("X_train.csv")
model = joblib.load("model-data/20220825/rf.model")

data = pd.DataFrame(
    [
        [497.3914855353, 254.7762608292, 148.0338606126, 425.269976021],
        [500.5479805353, 245.6787654435, 137.4658754543, 435.269976021],
        [503.3943446643, 252.6357876754, 125.4356787442, 438.269976021],
        [488.3138793443, 260.2343254676, 117.4356789763, 427.269976021],
        [478.9545765343, 258.4556765765, 120.0987655242, 430.269976021]
    ],
    columns=["ingot", "mould", "oil_pressure", "bucket"])
# print(data)

data_ = []
cols = ['ingot', 'mould', 'oil_pressure', 'bucket']
cols_ = []
agg_funcs = ["mean", "median", "max", "min", "std", "var", "sum", "skew", "kurt",
             mode, _ptp, _iqr, _sem, "count_nonzero"]
agg_func_names = ["mean", "median", "max", "min", "std", "var", "sum", "skew", "kurt",
                  "mode", "ptp", "iqr", "sem", "count_nonzero"]
final_funcs = ["ingot_mean", "ingot_max", "ingot_sum", "ingot_mode", "ingot_median", "ingot_min",
               "bucket_sum", "mould_sum", "mould_skew", "ingot_skew"]
for col in cols:
    for agg_name in agg_func_names:
        cols_.append("{}_{}".format(col, agg_name))
# print(cols_)

for col in cols:
    data_ = data_ + (list(data[col].agg(agg_funcs)))

# data_agg = data.agg(agg_funcs)

data_df = pd.DataFrame(data_).T
data_df.columns = cols_
data_df = data_df[final_funcs]
# print(data_df.to_numpy()[0])
# exit(0)

print(model.predict_proba(data_df))

lime_explainer = lime_tabular.LimeTabularExplainer(
    training_data=np.array(X_train),
    feature_names=X_train.columns,
    class_names=['A', 'B'],
    mode='classification'
)

lime_exp = lime_explainer.explain_instance(
    data_row=data_df.to_numpy()[0],
    predict_fn=model.predict_proba
)

print(lime_exp.predict_proba)
print(lime_exp.local_exp)
print(lime_exp.mode)
print(lime_exp.score)
print(lime_exp.random_state)
print(lime_exp.intercept)
print(lime_exp.class_names)
print(lime_exp.domain_mapper)
print(lime_exp.local_pred)
print(lime_exp.top_labels)
print(lime_exp.as_list())
print(lime_exp.as_map())
print(lime_exp.available_labels())

# import pandas as pd
#
# lst = [('ingot_skew > 0.86', -0.12306329545015376), ('ingot_margin > 0.00', 0.0038502934003718917),
#        ('mould_crest <= 1.01', -0.0035236557259557093), ('ingot_rms > 446.89', -0.0028727000533908674),
#        ('mould_ptp <= 3.03', -0.001926353231187214), ('ingot_mean > 438.19', 0.0017806528198153612),
#        ('mould_max > 347.59', -0.0012923867098006293), ('ingot_sum <= 34044.44', 0.0007447396846282722),
#        ('mould_sum <= 25721.62', 0.00022684396229667971), ('ingot_median > 485.41', -5.781280298212527e-05)]
# cols = ["condition", "impact value"]
# df = pd.DataFrame.from_records(lst, columns=cols)
# print(df)
# print(type(df["condition"].iloc[0]))
