import numpy as np
import pandas as pd
from statistics import mode
from scipy.stats import iqr, sem


class TimeDomain:

    def __init__(self, df: pd.DataFrame, become_one_row: bool = True):
        self.df = df
        self.become_one_row = become_one_row

    def ptp(self, x):
        return np.ptp(x.values)

    def iqr(self, x):
        return iqr(x.values)

    def sem(self, x):
        return sem(x.values)

    def analysis(self):
        """
        mean: 平均
        median:
        max: 最大
        min: 最小
        std: 標準差
        var: 變異數
        sum: 總和
        skew: 偏度
        kurt: 峰度
        mode: 眾數
        ptp: 全距
        iqr: 四分位距
        sem: 平均值的標準誤差
        count_nonzero: 非零個數
        """

        agg_func = ["mean", "median", "max", "min", "std", "var", "sum", "skew", "kurt",
                    mode, self.ptp, self.iqr, self.sem, "count_nonzero"]
        df_agg = self.df.agg(agg_func)

        new_index = [idx.replace("_", "") for idx in df_agg.index]
        df_agg.index = new_index

        if self.become_one_row:
            cols = df_agg.columns
            index = df_agg.index
            new_cols = ["{}_{}".format(col, idx) for col in cols for idx in index]

            data_lst = []
            for col in cols:
                data_lst = data_lst + list(df_agg[col])
            df_agg = pd.DataFrame(data_lst).T
            df_agg.columns = new_cols

        return df_agg


# data = pd.read_csv("unlabeled-data/May-9-data.csv")
# print(data.head(10))
# td = TimeDomain(data)
# df = td.analysis()
# print(df)
# print(df.shape)
# print(df.columns)

