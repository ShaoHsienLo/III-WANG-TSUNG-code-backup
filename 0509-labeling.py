import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from statistics import mode
from scipy.stats import iqr, sem


def _ptp(x):
    return np.ptp(x.values)


def _iqr(x):
    return iqr(x.values)


def _sem(x):
    return sem(x.values)


# Read csv file and define some settings
# Set first ingot index, total ingot quantity and quality results
df = pd.read_csv('unlabeled-data/May-9-data.csv')
start_index = df[df['Timestamp'] >= '2022-05-09 14:51:00'].index[0]
ingot_quantity = 36
quality_results = [
    ['XB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'],
    ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'],
    ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'],
    ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BX']
]
label_mapping = {
    "XA": "A", "XB": "B", "XC": "C",
    "AX": "A", "BX": "B", "CX": "C",
    "AA": "A", "AB": "A", "AC": "A",
    "BB": "B", "BC": "B", "CC": "C"
}

# Fegure out ingot ingot_peaks range: method 2
state = 'working'
ingot_index = []
for i, ingot_tem in enumerate(df['ingot']):
    if (ingot_tem < 320) & (state == 'working'):
        state = 'not working'
        ingot_index.append(i)
    elif (ingot_tem > 390) & (state == 'not working'):
        state = 'working'
        ingot_index.append(i)
if ingot_index[0] != 0:
    ingot_index = [0] + ingot_index
if len(ingot_index) % 2 != 0:
    ingot_index = ingot_index[:-1]
print('ingot_index: ', ingot_index)

ingot_peak_index = []
idx = 0
while idx != len(ingot_index):
    if ingot_index[idx + 1] - ingot_index[idx] > 20:
        ingot_peak_index.append([ingot_index[idx], ingot_index[idx + 1]])
    idx = idx + 2
print('ingot_peak_index: ', ingot_peak_index)

# Fegure out oil pressure the highest peak
oil_pressure_peaks, _ = find_peaks(df['oil_pressure'], height=90)
oil_pressure_peak_index = []
for i, lst in enumerate(ingot_peak_index):
    first_peak_idx = [peak for peak in oil_pressure_peaks if peak > lst[1]][1]
    oil_pressure_peak_index.append(first_peak_idx)
print('oil_pressure_peaks: ', oil_pressure_peak_index)

oil_pressure_end_index = []
for idx in oil_pressure_peak_index:
    i = idx + 1
    while (df['oil_pressure'][i] > 30) & (i < len(df['oil_pressure']) - 1):  # get the index of oil pressure < 30
        i = i + 1
    oil_pressure_end_index.append(i)
print('oil_pressure_end_index: ', oil_pressure_end_index)

"""
peaks format: [[ingot_start, ingot_end, oil_presuure_start, oil_pressure_end], ...], ...]
a aluminum data:
ingot data: ingot_start to ingot_end
oil_pressure, discharge, mould and bucket data: oil_pressure_start to oil_pressure_end
"""

# Check the lengths of ingot and oil pressure are same
assert len(oil_pressure_peak_index) == len(oil_pressure_end_index)
assert len(ingot_peak_index) == len(oil_pressure_end_index)

# Merge ingot and oil pressure data, check discharge temperature > 350
peaks = []
for i, lst in enumerate(ingot_peak_index):
    if df['discharge'][oil_pressure_peak_index[i]] > 350:
        peaks.append([lst[0], lst[1], oil_pressure_peak_index[i], oil_pressure_end_index[i]])
print('peaks: ', peaks)
print('peaks length: ', len(peaks))

# Check first ingot start index and total data length
for i, lst in enumerate(peaks):
    if lst[0] >= start_index:
        peaks = peaks[i:]
        break
assert len(peaks) >= ingot_quantity + 1
peaks = peaks[:ingot_quantity]
print('peaks: ', peaks)
print('peaks length: ', len(peaks))

"""
rules:
lst[1] - lst[0] > 20
lst[2] - lst[1] < 100
lst[3] - lst[2] > 20
"""

# Check the rules
correct = True
for i, lst in enumerate(peaks):
    if (lst[2] - lst[1] > 100) | (lst[3] - lst[2] < 20):
        print(lst)
        correct = False
assert correct

"""
lst:
0: ingot start index
1: ingot end index
2: oil pressure start index
3: oil pressure end index
"""

output = None
data_list = []
data_ = []
cols_ = []
cols = ['ingot', 'discharge', 'mould', 'oil_pressure', 'bucket']
agg_functions = ["mean", "median", "max", "min", "std", "var", "sum", "skew", "kurt",
                 mode, _ptp, _iqr, _sem, "count_nonzero"]
agg_func_names = ["mean", "median", "max", "min", "std", "var", "sum", "skew", "kurt",
                  "mode", "ptp", "iqr", "sem", "count_nonzero"]
for col in cols:
    for agg_name in agg_func_names:
        cols_.append("{}_{}".format(col, agg_name))
cols_ = cols_ + ["original label"]

for i, lst in enumerate(peaks):
    # Get every columns start and end index
    ingot_start_index = lst[0]
    ingot_end_index = lst[1]
    oil_pressure_start_index = lst[2]
    oil_pressure_end_index = lst[3]
    try:
        next_oil_pressure_start_index = peaks[i + 1][2]
    except IndexError as e:
        next_oil_pressure_start_index = oil_pressure_end_index

    # Get ingot data
    ingot_data = df['ingot'].iloc[ingot_start_index:ingot_end_index]
    # Get oil pressure, mould and bucket data
    oil_pressure_data = df['oil_pressure'].iloc[ingot_start_index:ingot_end_index]
    mould_data = df['mould'].iloc[ingot_start_index:ingot_end_index]
    bucket_data = df['bucket'].iloc[ingot_start_index:ingot_end_index]
    # Get discharge data
    discharge_data = df['discharge'].iloc[ingot_start_index:ingot_end_index]
    # Merge all data
    data = {
        "ingot": ingot_data,
        "oil_pressure": oil_pressure_data,
        "mould": mould_data,
        "bucket": bucket_data,
        "discgage": discharge_data
    }

    # Time domain analysis
    for k, v in data.items():
        data_ = data_ + list(v.agg(agg_functions))
    data_ = data_ + quality_results[i]

    data_list.append(data_)
    data_ = []

data_list = pd.DataFrame(data_list, columns=cols_)
data_list["final label"] = data_list["original label"].map(label_mapping)
print(data_list)
data_list.to_csv("labeled-data/May-9-labeled-data.csv", index=False)
