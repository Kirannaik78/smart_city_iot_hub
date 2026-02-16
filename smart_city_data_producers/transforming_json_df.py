import glob
import pandas as pd
import json
import csv


def convert_json_to_df(json_data):
    pass


def read_data(file_path):

    rows= []
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            print(line)
            if not line:
                continue

            try:
                data = json.loads(line)

                for ts, val in data.items():
                    rows.append({'timestamp':ts, "value":val})
            except json.JSONDecodeError as e:
                print(f"Error on line {line_num}: {e}")
    
    file_name = file_path.rsplit('/', 1)
    file_path = file_name[0]+"/parquet_data/"+file_name[1].split('.')[0]+'.parquet'

    df = pd.DataFrame(rows)

    df.to_parquet(file_path, engine='pyarrow', index=False)
    


def main(folder_path):
    for path in glob.glob(folder_path, recursive=True):
        read_data(path)

if __name__ == "__main__":
    folder_path = "/home/kiran/Documents/smart_city_data/raw_weather_data_aarhus/*.txt"
    main(folder_path)