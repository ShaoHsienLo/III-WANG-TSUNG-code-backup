import logging

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import json
from loguru import logger
from matplotlib import dates as mdates
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from matplotlib import colors as mcolors
import math
from datetime import timedelta
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation

# Read file
logger.info('Reading file ...')
df = pd.read_csv('Jan_processed_data.csv')

# Standardizing
logger.info('Standardizing data ...')
df_st = StandardScaler().fit_transform(df.values)
df_st = pd.DataFrame(df_st, columns=df.columns)

# PCA: ratio > 0.9
logger.info('PCA-ing ...')
n_component = 4
pca = PCA(n_component)
pca_data = pca.fit_transform(df_st)
pca_data = pd.DataFrame(data=pca_data)

# Kmeans
logger.info('KMeans clustering ...')
n_cluster = 3
kmeans_pca = KMeans(n_clusters=n_cluster, init='k-means++', random_state=42)
kmeans_pca.fit(pca_data)

# Kmeans Clustering with PCA Results
logger.info('Merge KMeans clustering with PCA results ...')
df_pca_data = pd.concat([df_st, pca_data], axis=1)
df_pca_data.columns.values[-n_component:] = ['Component {}'.format(i) for i in range(1, n_component + 1)]
df_pca_data['K-means PCA'] = kmeans_pca.labels_

logger.info('Generate plot dataframe ...')
df_plot_pca_data = df_pca_data[['Component {}'.format(i) for i in range(1, n_component + 1)]]

# Plot data by PCA components
logger.info('Plotting data by PCA components ...')
for col_1 in df_plot_pca_data.columns:
    for col_2 in df_plot_pca_data.columns[1:]:
        plt.figure(figsize=(10, 8))
        # sns.scatterplot(data=df_plot_pca_data, x=i, y=j, hue=df_pca_data['K-means PCA'],
        #                 palette=['g', 'r', 'c'])
        sns.scatterplot(data=df_plot_pca_data, x=col_1, y=col_2, hue=df_pca_data['K-means PCA'],
                        palette=['g', 'r', 'c'])
        plt.title('Clusters by PCA components')
        # plt.show()
        plt.savefig('Component {}-{}.png'.format(col_1, col_2))
        plt.close()

        break
    break

