import requests
import mariadb
import sys
import re

try:
    conn = mariadb.connect(
        user="lguplus7",
        password="lg7p@ssw0rd~!",
        host="localhost",
        port=3310,
        database="cp_data"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()

url = "https://apihub.kma.go.kr/api/typ01/cgi-bin/url/nph-aws2_min"
params = {
    'tm2': '202302010900',
    'stn': '0',
    'disp': '0',  # 공백 구분 데이터
    'help': '1',
    'authKey': 'Y2bfFcLTSJam3xXC07iWdg'
}

response = requests.get(url, params=params)
response.raise_for_status()

lines = response.text.strip().split('\n')

# 헤더 라인 찾기 (주석 # 제거 후 검색)
header_line = None
for i, line in enumerate(lines):
    stripped = line.lstrip('#').strip()
    if not stripped:
        continue
    if 'YYMMDDHHMI' in stripped and 'STN' in stripped:
        header_line = stripped
        header_index = i
        break

if header_line is None:
    print("헤더를 찾지 못했습니다.")
    sys.exit(1)

columns = re.split(r'\s+', header_line)

# 헤더 다음 줄부터 데이터 시작
records = lines[header_index+1:]

for line_num, line in enumerate(records, start=1):
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    values = re.split(r'\s+', line)

    if len(values) != len(columns):
        print(f"데이터 라인 {line_num} 컬럼 수와 데이터 개수 불일치, 스킵: {line}")
        continue

    row = dict(zip(columns, values))

    yyyymmddhhmi = row.get('YYMMDDHHMI')
    stn = row.get('STN')

    if yyyymmddhhmi is None or stn is None:
        print(f"데이터 라인 {line_num} 필수 키 누락, 스킵")
        continue

    org_data = str(row)

    cur.execute(
        "SELECT COUNT(*) FROM tb_weather_aws1 WHERE yyyymmddhhmi = ? AND stn = ?",
        (yyyymmddhhmi, stn)
    )
    (count,) = cur.fetchone()

    if count == 0:
        cur.execute(
            """
            INSERT INTO tb_weather_aws1 (
                yyyymmddhhmi, stn, wd1, ws1, wds, wss, wd10, ws10, ta, re,
                rn_15m, rn_60m, rn_12h, rn_day, hm, pa, ps, td, org_data, update_dt
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
            """,
            (
                yyyymmddhhmi,
                stn,
                row.get('WD1', '0'),
                row.get('WS1', '0'),
                row.get('WDS', '0'),
                row.get('WSS', '0'),
                row.get('WD10', '0'),
                row.get('WS10', '0'),
                row.get('TA', '0'),
                row.get('RE', '0'),
                row.get('RN-15m', '0'),
                row.get('RN-60m', '0'),
                row.get('RN-12H', '0'),
                row.get('RN-DAY', '0'),
                row.get('HM', '0'),
                row.get('PA', '0'),
                row.get('PS', '0'),
                row.get('TD', '0'),
                org_data
            )
        )
        print(f"Inserted: {yyyymmddhhmi} / {stn}")
    else:
        print(f"Skipped duplicate: {yyyymmddhhmi} / {stn}")

conn.commit()
cur.close()
conn.close()







# import requests
# import mariadb
# import sys
# import re
# import json

# try:
#     conn = mariadb.connect(
#         user="lguplus7",
#         password="lg7p@ssw0rd~!",
#         host="localhost",
#         port=3310,
#         database="cp_data"
#     )
#     cur = conn.cursor()
# except mariadb.Error as e:
#     print(f"Error connecting to MariaDB Platform: {e}")
#     sys.exit(1)

# url = "https://apihub.kma.go.kr/api/typ01/cgi-bin/url/nph-aws2_min"
# params = {
#     'tm2': '202302010900',
#     'stn': '0',
#     'disp': '0',  # 공백 구분 데이터
#     'help': '1',
#     'authKey': 'Y2bfFcLTSJam3xXC07iWdg'
# }

# response = requests.get(url, params=params)
# response.raise_for_status()

# lines = response.text.strip().split('\n')

# header_line = None
# for i, line in enumerate(lines):
#     stripped = line.lstrip('#').strip()
#     if not stripped:
#         continue
#     if 'YYMMDDHHMI' in stripped and 'STN' in stripped:
#         header_line = stripped
#         header_index = i
#         break

# if header_line is None:
#     print("헤더를 찾지 못했습니다.")
#     sys.exit(1)

# columns = re.split(r'\s+', header_line)
# print(f"Columns: {columns}")

# records = lines[header_index + 1:]

# for line_num, line in enumerate(records, start=1):
#     line = line.strip()
#     if not line or line.startswith('#'):
#         continue
#     values = re.split(r'\s+', line)

#     if len(values) != len(columns):
#         print(f"데이터 라인 {line_num} 컬럼 수와 데이터 개수 불일치, 스킵: {line}")
#         continue

#     row = dict(zip(columns, values))
#     yyyymmddhhmi = row.get('YYMMDDHHMI')
#     stn = row.get('STN')

#     if yyyymmddhhmi is None or stn is None:
#         print(f"데이터 라인 {line_num} 필수 키 누락, 스킵")
#         continue

#     org_data = json.dumps(row, ensure_ascii=False)

#     try:
#         cur.execute(
#             "SELECT COUNT(*) FROM tb_weather_aws1 WHERE yyyymmddhhmi = ? AND stn = ?",
#             (yyyymmddhhmi, stn)
#         )
#         (count,) = cur.fetchone()

#         if count == 0:
#             cur.execute(
#                 """
#                 INSERT INTO tb_weather_aws1 (
#                     yyyymmddhhmi, stn, wd1, ws1, wds, wss, wd10, ws10, ta, re,
#                     rn_15m, rn_60m, rn_12h, rn_day, hm, pa, ps, td, org_data, update_dt
#                 ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
#                 """,
#                 (
#                     yyyymmddhhmi,
#                     stn,
#                     row.get('WD1', '0'),
#                     row.get('WS1', '0'),
#                     row.get('WDS', '0'),
#                     row.get('WSS', '0'),
#                     row.get('WD10', '0'),
#                     row.get('WS10', '0'),
#                     row.get('TA', '0'),
#                     row.get('RE', '0'),
#                     row.get('RN-15m', '0'),
#                     row.get('RN-60m', '0'),
#                     row.get('RN-12H', '0'),
#                     row.get('RN-DAY', '0'),
#                     row.get('HM', '0'),
#                     row.get('PA', '0'),
#                     row.get('PS', '0'),
#                     row.get('TD', '0'),
#                     org_data
#                 )
#             )
#             print(f"Inserted: {yyyymmddhhmi} / {stn}")
#         else:
#             print(f"Skipped duplicate: {yyyymmddhhmi} / {stn}")

#     except mariadb.Error as e:
#         print(f"DB 오류: {e} - 데이터 라인 {line_num}")

# conn.commit()
# cur.close()
# conn.close()
