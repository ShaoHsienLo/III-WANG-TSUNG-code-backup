import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os
from loguru import logger
from scipy.signal import find_peaks


df = pd.read_csv('Jul-5-6-data.csv')
# df = df[:10000]

fig = go.Figure()

c_list = ['#1f77b4', '#ff7f0e', '#d62728', '#9467bd', '#946700']
y_axes_list = ['ingot', 'discharge', 'mould', 'oil_pressure', 'bucket']
y_axes_name_list = ['擠錠溫度', '出料溫度', '模具溫度', '油缸壓力', '盛錠桶溫度']


fig.add_trace(go.Scatter(
    x=df.index,
    y=df['ingot'],
    name="擠錠溫度",
    marker=dict(size=5, color=c_list[0])
))

for i in range(1, len(y_axes_list)):
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[y_axes_list[i]],
        name=y_axes_name_list[i],
        yaxis="y{}".format(i + 1),
        marker=dict(size=5, color=c_list[i])
    ))

# Create axis objects
fig.update_layout(
    xaxis=dict(
        domain=[0.3, 0.7]
    ),
    yaxis=dict(
        title="擠錠溫度",
        titlefont=dict(
            color=c_list[0]
        ),
        tickfont=dict(
            color=c_list[0]
        )
    ),
    yaxis2=dict(
        title="出料溫度",
        titlefont=dict(
            color=c_list[1]
        ),
        tickfont=dict(
            color=c_list[1]
        ),
        anchor="free",
        overlaying="y",
        side="left",
        position=0.2
    ),
    yaxis3=dict(
        title="模具溫度",
        titlefont=dict(
            color=c_list[2]
        ),
        tickfont=dict(
            color=c_list[2]
        ),
        anchor="x",
        overlaying="y",
        side="right"
    ),
    yaxis4=dict(
        title="油缸壓力",
        titlefont=dict(
            color=c_list[3]
        ),
        tickfont=dict(
            color=c_list[3]
        ),
        anchor="free",
        overlaying="y",
        side="right",
        position=0.8
    ),
    yaxis5=dict(
        title="盛錠桶溫度",
        titlefont=dict(
            color=c_list[4]
        ),
        tickfont=dict(
            color=c_list[4]
        ),
        anchor="free",
        overlaying="y",
        side="right",
        position=0.9
    )
)

# Update layout properties
fig.update_layout(
    title={
        'text': "旺欉鋁擠資料 (2022/7/5 00:00 ~ 2022/7/7 00:00)",   # 标题名称
        'y': 0.95,  # 位置，坐标轴的长度看做1
        'x': 0.5,
        'xanchor': 'center',   # 相对位置
        'yanchor': 'top'},
    xaxis_title="時間 (秒)",
    # yaxis_title="Y Axis Title",
    # title_text="multiple y-axes example",
    width=1200,
    legend=dict(x=1, y=1)
)

# fig.show()
fig.write_html('0705-06-plot.html')
