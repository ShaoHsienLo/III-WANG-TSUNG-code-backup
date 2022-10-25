import json
import time

import numpy as np
import paho.mqtt.client as mqtt
import pandas as pd
from scipy.stats import kurtosis
from sqlalchemy import create_engine, types
from datetime import datetime
import joblib


data = pd.DataFrame()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # If we lose connection or reconnect, the terminal will resubscribe
    client.subscribe("fuck")


def on_message(client, userdata, msg):
    global data

    messages = json.loads(msg.payload.decode("utf-8"))
    df = pd.DataFrame(messages)
    t = df["Timestamp"].iloc[-1]
    df_mean = pd.DataFrame(df.mean(numeric_only=True)).transpose()
    df_mean.insert(0, "timestamp", t)
    df_mean = df_mean.drop(columns=["pie"])
    data = df_mean

    # print(msg.topic + " " + msg.payload.decode("utf-8")))
    # print("Done")
    # time.sleep(1)


def load_model():
    return joblib.load("rf.model")


def insert_data_to_postgres(data):
    engine = create_engine('postgresql://postgres:123456@localhost:5432/postgres')
    sql_types = {
        "timestamp": types.TIMESTAMP, "ingot": types.FLOAT, "discharge": types.FLOAT,
        "mould": types.FLOAT, "oil_pressure": types.FLOAT, "bucket": types.FLOAT,
        "E_temperature": types.FLOAT, "E_humidity": types.FLOAT
    }
    try:
        data.to_sql('realtime', engine, if_exists="append", index=False, dtype=sql_types)
    except ValueError as e:
        data.to_sql('realtime', engine, index=False, dtype=sql_types)
    # print("Insert data done.")


def insert_results_to_postgres(time_df):
    engine = create_engine('postgresql://postgres:123456@localhost:5432/postgres')
    sql_types = {
        "ingot_start_time": types.TIMESTAMP, "ingot_end_time": types.TIMESTAMP, 
        "oil_pressure_start_time": types.TIMESTAMP, "oil_pressure_end_time": types.TIMESTAMP, 
        "result": types.VARCHAR, "score": types.FLOAT
    }
    # print(time_df)
    # print(type(time_df))
    df = pd.DataFrame(time_df).T
    # print(df)
    # print(type(df))
    try:
        df.to_sql('quality', engine, if_exists="append", index=False, dtype=sql_types)
    except ValueError as e:
        df.to_sql('quality', engine, index=False, dtype=sql_types)
    print("Insert results done.")


def predict(time_df):
    engine = create_engine('postgresql://postgres:123456@localhost:5432/postgres')
    conn = engine.connect()
    query = """
        select * from public.realtime 
        where timestamp >= '{}' and timestamp <= '{}'
    """.format(time_df["ingot_start_time"].iloc[0], time_df["oil_pressure_end_time"].iloc[0])
    # print(query)
    query_ = conn.execute(query)
    df = pd.DataFrame([dict(i) for i in query_])
    df = df.drop_duplicates()
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S")
    print("query data: \n", df.head())

    ingot_data = df.loc[
        (df["timestamp"] > time_df["ingot_start_time"].iloc[0]) &
        (df["timestamp"] < time_df["ingot_end_time"].iloc[0]),
        "ingot"
    ]
    other_features_data = df[
        (df["timestamp"] > time_df["oil_pressure_start_time"].iloc[0]) &
        (df["timestamp"] < time_df["oil_pressure_end_time"].iloc[0])
    ]
    input_data = {
        "ingot": ingot_data,
        "mould": other_features_data["mould"],
        "oil_pressure": other_features_data["oil_pressure"],
        "bucket": other_features_data["bucket"]
    }
    # print(input_data)
    data_ = []
    cols = ['ingot', 'mould', 'oil_pressure', 'bucket']
    cols_ = []
    agg_funcs = ["mean", "median", "sum", "std", "min", "max", "skew", "kurt", "var", rms, ptp, crest, shape, impulse,
                 margin]
    agg_func_names = ["mean", "median", "sum", "std", "min", "max", "skew", "kurt", "var", "rms", "ptp", "crest",
                      "shape", "impulse", "margin"]
    final_funcs = ["ingot_mean", "ingot_rms", "ingot_median", "ingot_sum", "ingot_skew", "ingot_margin", "mould_max",
                   "mould_ptp", "mould_sum", "mould_crest"]
    for col in cols:
        for agg_name in agg_func_names:
            cols_.append("{}_{}".format(col, agg_name))
    for k, v in input_data.items():
        data_ = data_ + (list(v.agg(agg_funcs)))

    # print(data_)
    data_df = pd.DataFrame(data_).T
    data_df.columns = cols_
    # print(data_df)
    data_df = data_df[final_funcs]
    print("data_df: \n", data_df)

    model = load_model()
    quality = ""
    score = 0
    quality_mapping = {0: "A", 1: "B", 2: "C"}

    y_prob = model.predict_proba(data_df)
    y_prob = y_prob[0]
    # print(y_prob)
    max_index = np.argmax(y_prob).item()

    quality = quality_mapping[max_index]
    score = y_prob[max_index] * 100
    # print(quality)
    # print(score)

    return quality, score


def skew(x):
    return skew(np.array(x))


def rms(x):
    return np.sqrt(np.mean(np.power(x.values, 2)))


def ptp(x):
    return np.ptp(x.values)


def kur(x):
    return kurtosis(np.array(x.values))


def crest(x):
    return max(x.values) / np.sqrt(np.mean(np.power(x.values, 2)))


def shape(x):
    return np.sqrt(np.mean(np.power(x.values, 2))) / np.mean(np.abs(x.values))


def impulse(x):
    return max(x.values) / np.mean(np.abs(x.values))


def margin(x):
    return max(x.values) / np.power(np.mean(np.abs(x.values)), 2)


def connect():
    client = mqtt.Client(transport="websockets")
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("iii", "iii05076416")
    client.loop_start()
    client.connect("192.168.0.135", 8087, 60)
    # ...
    times = {
        "ingot_start_time": [None, None],
        "ingot_end_time": [None, None],
        "oil_pressure_start_time": [None, None],
        "oil_pressure_end_time": [None, None],
        "result": [None, None],
        "score": [None, None]
    }
    time_df = pd.DataFrame.from_dict(times, orient="index").T

    while True:
        if not data.empty:
            insert_data_to_postgres(data)

            # current ingot start and end
            if (data["ingot"].iloc[0] > 390) & (time_df["ingot_start_time"].iloc[0] is None):
                time_df["ingot_start_time"].iloc[0] = datetime.now()
                print("ingot start: \n", time_df)
            elif (data["ingot"].iloc[0] < 320) & (time_df["ingot_end_time"].iloc[0] is None) & \
                    (time_df["ingot_start_time"].iloc[0] is not None):
                if (datetime.now() - time_df["ingot_start_time"].iloc[0]).total_seconds() > 30.0:
                    time_df["ingot_end_time"].iloc[0] = datetime.now()
                else:
                    time_df["ingot_start_time"].iloc[0] = None
                print("ingot end: \n", time_df)
            elif (time_df["ingot_start_time"].iloc[0] is not None) & (time_df["ingot_end_time"].iloc[0] is not None):
                # oil pressure start and end
                if (data["oil_pressure"].iloc[0] > 120) & (time_df["oil_pressure_start_time"].iloc[0] is None):
                    time_df["oil_pressure_start_time"].iloc[0] = datetime.now()
                    print("oil pressure start: \n", time_df)
                elif (data["oil_pressure"].iloc[0] < 10) & (time_df["oil_pressure_end_time"].iloc[0] is None) & \
                        (time_df["oil_pressure_start_time"].iloc[0] is not None):
                    time_df["oil_pressure_end_time"].iloc[0] = datetime.now()
                    print("oil pressure end: \n", time_df)
                elif (time_df["oil_pressure_start_time"].iloc[0] is not None) & \
                        (time_df["oil_pressure_end_time"].iloc[0] is not None):
                    # 當前鋁錠4個時間都有
                    print("current ingot start and end times: \n", time_df)
                    # print(type(time_df))

                    quality, score = predict(time_df)
                    time_df["result"].iloc[0] = quality
                    time_df["score"].iloc[0] = score
                    insert_results_to_postgres(time_df.iloc[0])
                
                    print("time_df_o:\n", time_df)
                    assert len(time_df) == 2
                    df_ = pd.DataFrame([None, None, None, None, None, None]).T
                    df_.columns = ["ingot_start_time", "ingot_end_time", "oil_pressure_start_time", "oil_pressure_end_time", "result", "score"]
                    time_df = pd.concat([time_df, df_], ignore_index=True, axis=0)
                    # time_df = pd.concat([time_df, pd.DataFrame([None, None, None, None, None, None]).T])
                    time_df = time_df.iloc[1:]
                    time_df = time_df.reset_index(drop=True)
                    print("time_df_p:\n", time_df)
                    continue

                # next ingot start and end
                if (data["ingot"].iloc[0] > 390) & (time_df["ingot_start_time"].iloc[1] is None):
                    time_df["ingot_start_time"].iloc[1] = datetime.now()
                    print("ingot 1 start: \n", time_df)
                elif (data["ingot"].iloc[0] < 320) & (time_df["ingot_end_time"].iloc[1] is None) & \
                        (time_df["ingot_start_time"].iloc[1] is not None):
                    if (datetime.now() - time_df["ingot_start_time"].iloc[1]).total_seconds() > 30.0:
                        time_df["ingot_end_time"].iloc[1] = datetime.now()
                    else:
                        time_df["ingot_start_time"].iloc[1] = None
                    print("ingot 1 end: \n", time_df)

        time.sleep(1)
    # ...
    client.loop_stop()


if __name__ == "__main__":
    connect()
