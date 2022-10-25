import json
import paho.mqtt.client as mqtt
import random
import time
import datetime

import pandas as pd
from sqlalchemy import create_engine


def get_quality_from_potgres():
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    result = engine.execute('SELECT result FROM public.quality order by timestamp desc limit 6')
    rows = result.fetchall()
    df = pd.DataFrame(rows, columns=rows[0].keys())
    return df


# quality依序為：當前 → 前一個 → 前兩個 → 前三個 → 前四個 → 前五個 品質結果，共6個
qualities = get_quality_from_potgres()
qualities = list(qualities["result"])
print(qualities)
mapping = {"A": 0, "B": 1, "C": 2}
result = map(lambda x: mapping[x], qualities)
print(list(result))

# ISOTIMEFORMAT = "%Y-%m-%d %H:%M:%S"
#
# client = mqtt.Client(transport="websockets")
# # transport="websockets"
# client.username_pw_set("iii", "iii05076416")
# client.connect("192.168.0.135", 8087, 60)
#
# while True:
#     payload = {
#         'timestamp': datetime.datetime.now().timestamp(),
#         'topic': 'fuck',
#         'quality_now': random.randint(0, 2),
#         'quality_previous1': random.randint(0, 2),
#         'quality_previous2': random.randint(0, 2),
#         'quality_previous3': random.randint(0, 2),
#         'quality_previous4': random.randint(0, 2),
#         'quality_previous5': random.randint(0, 2)
#     }
#     print(json.dumps(payload))
#     client.publish("qualitytopic", json.dumps(payload))
#     time.sleep(30)
