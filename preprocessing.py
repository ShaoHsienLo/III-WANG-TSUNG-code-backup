import json

import pandas as pd
import os


def process_json_files():
    read_path = r"C:\Users\samuello\Downloads\III\旺欉\data\20220905-1007\1007"
    write_path = r"C:\Users\samuello\Downloads\III\旺欉\code\data"
    files = os.listdir(read_path)
    for file in files:
        print('Proccessing {} ...'.format(file))
        with open(os.path.join(read_path, file), 'r') as rf:
            write_filename = file[:-5] + '.txt'
            with open(os.path.join(write_path, write_filename), 'w') as wf:
                lines = rf.readlines()
                for line in lines:
                    try:
                        line = line[:-2]
                        assert json.loads(line)
                        wf.write(line)
                        wf.write('\n')
                    except Exception as e:
                        pass


def convert_txt_to_csv():
    read_path = r"C:\Users\samuello\Downloads\III\旺欉\code\data"
    # write_path = r"C:\Users\samuello\Downloads\III\旺欉\code\unlabeled-data"
    files = os.listdir(read_path)
    df = pd.DataFrame()
    for file in files:
        print('Proccessing {} ...'.format(file))
        data = pd.read_json(os.path.join(read_path, file), lines=True)
        if not df.empty:
            df = pd.concat([df, data])
        else:
            df = data
    df.to_csv("Oct-7-data.csv", index=False)


def precess_groupby_data():
    path = r'C:\Users\samuello\Downloads\III\旺欉\code\unlabeled-data\132'
    files = os.listdir(path)

    for file in files:
        cols = ['Timestamp', 'ingot', 'discharge', 'mould', 'oil_pressure', 'bucket', 'E_temperature', 'E_humidity']

        data = pd.read_csv(os.path.join(path, file))
        data = data.drop(columns=['pie'])
        data = data.groupby(by=['Timestamp'], as_index=False).mean()
        data = data[cols]
        data = data.reset_index(drop=True)

        data.to_csv(file, index=False)


# process_json_files()
# convert_txt_to_csv()
# precess_groupby_data()









