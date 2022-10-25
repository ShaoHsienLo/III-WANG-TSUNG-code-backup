from redmail import outlook
import rsa
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
from loguru import logger


def get_last_update_timestamp_from_potgres():
    engine = create_engine('postgresql://postgres:123456@localhost:5432/postgres')
    result = engine.execute('SELECT ingot_start_time FROM public.quality order by ingot_start_time desc limit 1')
    rows = result.fetchall()
    df = pd.DataFrame(rows, columns=rows[0].keys())
    last_update_timestamp = pd.to_datetime(df["ingot_start_time"].iloc[0], format="%Y-%m-%d %H:%M:%S")
    return last_update_timestamp

logger.add("logs.log",rotation="500MB", encoding="utf-8", enqueue=True, retention="30 days")
logger.info("Check!")

today = datetime.now()
now_day = today.day
weekday = today.weekday()

# Get last update time
last_update_timestamp = get_last_update_timestamp_from_potgres()
last_update_day = last_update_timestamp.day

# 上次更新日期早於當天日期，且當天為平日
send_mail = False
if (now_day > last_update_day) & (weekday <= 5):
    send_mail = True
else:
    logger.info("Checked.")

# Send mail
if send_mail:
    password = b'\x8aqm\x96\xec\xe4R\xad\xc5{r\x06%;\xf7L2T\x0b5\x97\x9a}\x9f\xb73\xc4F\xb7\x01\x89\xc9\xe3P`\x06\x12' \
               b'\x9a\xe9\x94\x03\xcfS\xb3i\xcco\xe8T\xfcX\xdah|\xe2\x04\xbc\xea\x99\x13X}\xd9?'
    with open("privateKey.pem", "rb") as f:
        privateKey = f.read()
    privkey = rsa.PrivateKey.load_pkcs1(privateKey)
    password = rsa.decrypt(password, privkey).decode()

    outlook.username = "samuello@iii.org.tw"
    outlook.password = password

    outlook.send(
        receivers=["samuello@iii.org.tw"],
        subject="[警告]旺欉資料未更新",
        text="偵測到即時資料未更新至Server資料庫，上次更新時間為{}，可能是IPC或Server未開機或其他問題，敬請盡速解決。".format(
            last_update_timestamp.strftime("%Y-%m-%d %H:%M:%S"))
    )

    logger.info("Send mail.")

