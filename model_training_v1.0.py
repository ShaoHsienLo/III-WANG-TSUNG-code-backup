import random
import pandas as pd
import os
import joblib
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.tree import export_graphviz
import pydot
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from imblearn.combine import SMOTEENN
from sklearn.feature_selection import SelectKBest, f_classif
from lime.lime_tabular import LimeTabularExplainer
# from gaussiancopula_model import load_gaussian_copula_model

# pd.set_option('display.max_rows', 100)


def read_file(path, file):
    df = pd.read_csv(os.path.join(path, file))
    return df


def handle_na_values(df):
    df_handle_na = df.fillna(method="bfill")
    return df_handle_na


def handle_categorical_data(df_handle_na, label="label"):
    labelencoder = LabelEncoder()
    df_handle_na[label] = labelencoder.fit_transform(df_handle_na[label])
    df_encoded = df_handle_na.copy()
    target_names = labelencoder.classes_
    return df_encoded, target_names


def select_k_best(df_encoded, k=2, label="label"):
    X = df_encoded.drop(columns=label)
    y = df_encoded[label]
    fs = SelectKBest(score_func=f_classif, k=k)
    fs.fit(X, y)
    mask = fs.get_support()
    features_selected = []
    for bool, col in zip(mask, X.columns):
        if bool:
            features_selected.append(col)
    df_selected = pd.concat([df_encoded[features_selected], y], axis=1)
    # print(df_selected)
    return df_selected


def split_data(df, label="label"):
    random_state = random.randint(0, 100)
    # random_state = 42
    X = df.drop(columns=[label])
    y = df[label]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state, stratify=y)
    print("Total data set: ", X.shape)
    print("Training data set: ", X_train.shape)
    print("Testing data set: ", X_test.shape)
    return X_train, X_test, y_train, y_test


def normalization(X_train, X_test):
    scale = MinMaxScaler()
    X_train_norm = pd.DataFrame(scale.fit_transform(X_train), columns=X_train.columns)
    X_test_norm = pd.DataFrame(scale.transform(X_test), columns=X_test.columns)
    return X_train_norm, X_test_norm


def pca(X_train_norm):
    pca = PCA(n_components=0.95, svd_solver="full")
    X_pca = pca.fit_transform(X_train_norm)
    cols = ["pca_{}".format(i) for i in range(pca.n_components_)]
    X_train_pca = pd.DataFrame(X_pca, columns=cols, index=X_train_norm.index)
    # print("explained_variance_ratio_:\n", list(pca.explained_variance_ratio_))
    # print("explained_variance_ratio_ cumsum:\n", list(np.cumsum(pca.explained_variance_ratio_)))
    # print(X_train_pca)
    return pca, X_train_pca


def smoteenn(X_train_pca, y_train):
    sm = SMOTEENN()
    X_train_res, y_train_res = sm.fit_sample(X_train_pca, y_train)
    return X_train_res, y_train_res


def model_training(X_train_res, y_train_res):
    # rf = RandomForestClassifier(bootstrap=True, ccp_alpha=0.0, class_weight=None,
    #                             criterion='gini', max_depth=None, max_features='auto',
    #                             max_leaf_nodes=None, max_samples=None,
    #                             min_impurity_decrease=0.0, min_samples_leaf=1, min_samples_split=2,
    #                             min_weight_fraction_leaf=0.0, n_estimators=100,
    #                             n_jobs=-1, oob_score=False, random_state=8543, verbose=0, warm_start=False)
    # rf.fit(X_train_res, y_train_res)

    # lgbm = LGBMClassifier(boosting_type='gbdt', class_weight=None, colsample_bytree=1.0,
    #                       importance_type='split', learning_rate=0.1, max_depth=-1,
    #                       min_child_samples=20, min_child_weight=0.001, min_split_gain=0.0,
    #                       n_estimators=100, n_jobs=-1, num_leaves=31, objective=None,
    #                       random_state=5880, reg_alpha=0.0, reg_lambda=0.0, silent='warn',
    #                       subsample=1.0, subsample_for_bin=200000, subsample_freq=0)
    lgbm = LGBMClassifier()
    lgbm.fit(X_train_res, y_train_res)
    return lgbm


def explain_model(rf, X_train, X_test, target_names=None):
    X_train_ = X_train.copy().reset_index(drop=True)
    X_test_ = X_test.copy().reset_index(drop=True)
    explainer = LimeTabularExplainer(X_train_.values, feature_names=X_train_.columns, class_names=target_names)
    i = random.randint(0, X_test_.shape[0])
    exp = explainer.explain_instance(X_test_.iloc[i], rf.predict_proba)
    exp.save_to_file("./models/20221026/exp-lgbm.html")


def show_performances(rf, X_test_norm, y_test, target_names=None):
    y_pred = rf.predict(X_test_norm)

    print("Confusion metric:\n{}\n".format(classification_report(y_test, y_pred, target_names=target_names)))

    importrances = {'feature': X_test_norm.columns, 'importance': rf.feature_importances_}
    importrances_df = pd.DataFrame(data=importrances).sort_values(by=['importance'], ascending=False)
    print("Feature importances:\n{}\n".format(importrances_df))

    score = roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1])
    print("ROC SUC score:\n{}\n".format(score))


def visualization(rf, feature_list):
    tree = rf.estimators_[5]
    export_graphviz(tree, out_file='./visualization/tree.dot', feature_names=feature_list, rounded=True, precision=1)
    (graph,) = pydot.graph_from_dot_file('./visualization/tree.dot')
    graph.write_png('./visualization/tree.png')


def save_model(rf, model_name="rf.model"):
    joblib.dump(rf, "models/20221026/{}".format(model_name))


def load_model(model_name="rf.model"):
    model = joblib.load("models/20221026/{}".format(model_name))
    return model


# 讀檔
df_1_2 = read_file(r"C:\Users\samuello\Downloads\III\旺欉\code\labeled-data\1st-2st-labeling", "all-labeled-data.csv")
# df_3 = read_file(r"C:\Users\samuello\Downloads\III\旺欉\code\labeled-data\3st-labeling", "all-labeled-data.csv")
df_3 = read_file(r"C:\Users\samuello\Downloads\III\旺欉\code\labeled-data\3st-labeling", "all-labeled-data.csv")
df = pd.concat([df_1_2, df_3])

# df_sample = read_file(r"C:\Users\samuello\Downloads\III\旺欉\code\labeled-data", "gaussiancopula-sample-data.csv")
# target_number = 300
# sample_model = load_gaussian_copula_model()
# df_sample = sample_model.sample(num_rows=300 - len(df))
# df_sample.to_csv("labeled-data/gaussiancopula-sample-data.csv")
#
# df = pd.concat([df, df_sample])
df = df.drop(columns=df.filter(regex="discharge.*").columns)
df = df.drop(columns=df.filter(regex=".*_count_nonzero").columns)
df = df.drop(columns=["original label"])

# 處理遺失值
df_handle_na = handle_na_values(df)

# 處理類別資料
df_encoded, target_names = handle_categorical_data(df_handle_na, label="final label")

# 特徵選擇(降維)
df_selected = df_encoded
# df_selected = select_k_best(df_encoded, k=10, label="final label")

# 切分模型輸入資料與預測目標
X_train, X_test, y_train, y_test = split_data(df_selected, label="final label")

# 資料縮放
X_train_norm, X_test_norm = normalization(X_train, X_test)

# 處理資料維度
# pca, X_train_pca = pca(X_train_norm)

# 處理資料不平衡
X_train_res, y_train_res = smoteenn(X_train_norm, y_train)

# train = pd.concat([X_train_res, y_train_res], axis=1)
# test = pd.concat([X_test_norm, y_test.reset_index(drop=True)], axis=1)
# train.to_csv(os.path.join(
#     r"C:\Users\samuello\Downloads\III\旺欉\code\labeled-data\3st-labeling", "train.csv"
# ), index=False)
# test.to_csv(os.path.join(
#     r"C:\Users\samuello\Downloads\III\旺欉\code\labeled-data\3st-labeling", "test.csv"
# ), index=False)

# 模型訓練
# rf = model_training(X_train_res, y_train_res)
lgbm = model_training(X_train_res, y_train_res)

# 解釋模型
explain_model(lgbm, X_train, X_test, target_names=target_names)

# 儲存模型
save_model(lgbm, model_name="lgbm.model")

# 載入模型
rf_model = load_model(model_name="lgbm.model")

# 印出模型效能數據
show_performances(rf_model, X_test_norm, y_test, target_names=target_names)

# 輸出決策樹圖
# visualization(rf, X_train.columns)
