import duckdb
import os
import pandas as pd

duck_con = duckdb.connect("c:/data/duck_smb.db")
duck_con.execute("CREATE TABLE IF NOT EXISTS tb_smb_file AS SELECT * FROM read_csv('c:/data/info_data/1.csv');")
duck_con.execute("DELETE FROM tb_smb_file;")

csv_path = 'c:/data/info_data'
file_list = os.listdir( csv_path ) # 경로 내에 파일을 모두 불러옴
csv_file_list = [file for file in file_list if file.endswith('.csv')] # csv 확장자를 가진 파일로 새로운 리스트 생성

for csv_file_name in csv_file_list:
    csv_file_full = f'{csv_path}/{csv_file_name}'
    print(f'csv_file_name = {csv_file_full}')
    csv_df = pd.read_csv( csv_file_full )
    duck_con.execute("insert into tb_smb_file SELECT * FROM csv_df;")

print("csv loading complete")