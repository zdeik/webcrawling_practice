import os
import glob
import mariadb

# MariaDB 접속 정보
DB_CONFIG = {
    "user": "lguplus7",        # MariaDB 사용자명
    "password": "lg7p@ssw0rd~!",    # MariaDB 비밀번호
    "host": "localhost",       # DB 호스트
    "port": 3310,               # 포트 (기본 3306)
    "database": "cp_data"       # DB 이름
    
}

# CSV 파일이 있는 폴더 경로
CSV_FOLDER = r"C:\data\info_data"

# 테이블 컬럼 (col1 ~ col39)
columns = ",".join([f"col{i}" for i in range(1, 40)])

# DB 연결 (local_infile=True 필수)
conn = mariadb.connect(**DB_CONFIG, local_infile=True)
cur = conn.cursor()

# 폴더 안 모든 CSV 파일 경로
csv_files = glob.glob(os.path.join(CSV_FOLDER, "*.csv"))

if not csv_files:
    print("CSV 파일이 폴더에 없습니다.")
else:
    for file_path in csv_files:
        print(f"\n처리 중: {file_path}")

        # MariaDB가 읽을 수 있도록 경로 변환
        mysql_path = file_path.replace("\\", "\\\\")

        # CSV 삽입 전 레코드 수
        cur.execute("SELECT COUNT(*) FROM tb_smb_ods")
        before_count = cur.fetchone()[0]

        # LOAD DATA 실행
        sql = f"""
        LOAD DATA LOCAL INFILE '{mysql_path}'
        INTO TABLE tb_smb_ods
        CHARACTER SET utf8
        FIELDS TERMINATED BY ','
        OPTIONALLY ENCLOSED BY '"'
        LINES TERMINATED BY '\\r\\n'
        IGNORE 1 LINES
        ({columns});
        """
        cur.execute(sql)
        conn.commit()

        # 삽입 후 레코드 수
        cur.execute("SELECT COUNT(*) FROM tb_smb_ods")
        after_count = cur.fetchone()[0]

        inserted = after_count - before_count
        print(f"삽입 완료: {inserted} 건")

cur.close()
conn.close()
print("\n모든 CSV 파일 삽입 완료!")
