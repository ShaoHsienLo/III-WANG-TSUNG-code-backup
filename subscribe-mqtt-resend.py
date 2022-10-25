import json
import paho.mqtt.client as mqtt
import pandas as pd


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # If we lose connection or reconnect, the terminal will resubscribe
    client.subscribe("fuck")


def on_message(client, userdata, msg):
    messages = json.loads(msg.payload.decode("utf-8"))
    df = pd.DataFrame(messages)
    df = df.drop(columns=["pie"])
    # print(df)
    t = pd.to_datetime(df["Timestamp"].iloc[0], format='%Y-%m-%d %H:%M:%S')
    df_mean = pd.DataFrame(df.mean(numeric_only=True)).transpose()
    df_mean.insert(0, "timestamp", t.timestamp())
    df_mean.insert(1, "topic", "fuck")
    # print(df_mean)
    str_data = df_mean.to_json(orient="index")
    json_data = json.loads(str_data)
    json_data = json_data["0"]
    json_data = json.dumps(json_data)
    # print(type(json_data))
    print(json_data)
    client.publish("mytopic", json_data)

    # print(msg.topic + " " + msg.payload.decode("utf-8")))
    # time.sleep(1)


client = mqtt.Client(transport="websockets")
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("iii", "iii05076416")
client.connect("192.168.0.135", 8087, 60)
client.loop_forever()
