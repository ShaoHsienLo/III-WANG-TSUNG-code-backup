import pandas as pd

# labels = [
#     [
#         ['XB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'],
#         ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'],
#         ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'],
#         ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BX']
#     ],
#     [
#         ['XA'], ['AA'], ['AA'], ['AA'], ['AA'], ['AA'], ['AA'], ['AA'], ['AA'], ['AB'],
#         ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'],
#         ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'], ['BB'],
#         ['BX']
#     ],
#     [
#         ["XAA"], ["AAA"], ["AAA"], ["AAA"], ["AAA"], ["ABB"],
#         ["BBB"], ["BBB"], ["BBB"], ["BBB"], ["BBB"], ["BBB"], ["BBB"], ["BBB"],
#         ["BBB"], ["BBB"], ["BBB"], ["BBB"], ["BBB"], ["BBB"], ["BBB"], ["BBB"],
#         ["BBB"], ["BBB"], ["BBB"], ["BBB"], ["BBB"], ["BBB"], ["BBB"], ["BBB"],
#         ["BBX"]
#     ],
#     [
#         ["XB"],
#         ["BB"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"],
#         ["BB"], ["BB"],
#         ["BX"]
#     ],
#     [
#         ["XB"],
#         ["BB"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"],
#         ["BX"]
#     ],
#     [
#         ["XB"],
#         ["BB"], ["BB"], ["BB"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"],
#         ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"],
#         ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"], ["BB"],
#         ["BB"],
#         ["BX"]
#     ],
#     [
#         ["XB"],
#         ["BB"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AX"]
#     ],
#     [
#         ["XB"],
#         ["BB"], ["BB"], ["BB"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"], ["AA"],
#         ["AA"],
#         ["AX"]
#     ]
# ]

labels = [
    [
        'XB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB',
        'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB',
        'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB',
        'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BX'
    ],
    [
        'XA', 'AA', 'AA', 'AA', 'AA', 'AA', 'AA', 'AA', 'AA', 'AB',
        'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB',
        'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB', 'BB',
        'BX'
    ],
    [
        "XAA", "AAA", "AAA", "AAA", "AAA", "ABB",
        "BBB", "BBB", "BBB", "BBB", "BBB", "BBB", "BBB", "BBB",
        "BBB", "BBB", "BBB", "BBB", "BBB", "BBB", "BBB", "BBB",
        "BBB", "BBB", "BBB", "BBB", "BBB", "BBB", "BBB", "BBB",
        "BBX"
    ],
    [
        "XB",
        "BB",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA",
        "BB", "BB", "BB", "BB", "BB", "BB", "BB", "BB", "BB", "BB",
        "BB", "BB",
        "BX"
    ],
    [
        "XB",
        "BB",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA"
    ],
    [
        "XB",
        "BB", "BB", "BB",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA",
        "BB", "BB", "BB", "BB", "BB", "BB", "BB", "BB", "BB", "BB",
        "BB", "BB", "BB", "BB", "BB", "BB", "BB", "BB", "BB", "BB",
        "BB",
        "BX"
    ],
    [
        "XB",
        "BB",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AX"
    ],
    [
        "XB",
        "BB", "BB", "BB",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA", "AA",
        "AA",
        "AX"
    ]
]

three_segment_label_mapping = {
    "XAA": "A", "AAA": "A", "ABB": "B", "BBB": "B", "BBX": "B"
}

two_segment_label_mapping = {
    "XA": "A", "XB": "B", "XC": "C",
    "AX": "A", "BX": "B", "CX": "C",
    "AA": "A", "AB": "A", "AC": "A",
    "BB": "B", "BC": "B", "CC": "C"
}

df_0509 = pd.read_json("input-data/original data/0509.json", lines=True)
df_0704_1 = pd.read_json("input-data/original data/0704_1.json", lines=True)
df_0704_2 = pd.read_json("input-data/original data/0704_2.json", lines=True)
df_0905 = pd.read_json("input-data/original data/0905.json", lines=True)
df_0908 = pd.read_json("input-data/original data/0908.json", lines=True)
df_0922 = pd.read_json("input-data/original data/0922.json", lines=True)
df_1005 = pd.read_json("input-data/original data/1005.json", lines=True)
df_1007 = pd.read_json("input-data/original data/1007.json", lines=True)
dfs = [df_0509, df_0704_1, df_0704_2, df_0905, df_0908, df_0922, df_1005, df_1007]
# 0704_2: three segments, others: two segments
df_names = ["0509", "0704_1", "0704_2", "0905", "0908", "0922", "1005", "1007"]

for df, df_name, label in zip(dfs, df_names, labels):
    df["original_label"] = label
    if df_name != "0704_2":
        df["label"] = df["original_label"].map(two_segment_label_mapping)
    else:
        df["label"] = df["original_label"].map(three_segment_label_mapping)
    df.to_csv("./input-data/label data/{}.csv".format(df_name), index=False)


