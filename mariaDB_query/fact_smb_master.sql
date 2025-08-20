CREATE TABLE fact_smb_master (
    seq_no INT(11) NOT NULL AUTO_INCREMENT COMMENT '고유번호 ',
    smb_id CHAR(20) NOT NULL COMMENT '상가업소번호 ' COLLATE 'utf8mb4_general_ci',
    smb_name TEXT NOT NULL COMMENT '상호명 ' COLLATE 'utf8mb4_general_ci',
    smb_subnm VARCHAR(30) NOT NULL COMMENT '지점명 ' COLLATE 'utf8mb4_general_ci',
    cate1_cd CHAR(2) NOT NULL COMMENT '상권업종대분류코드 ' COLLATE 'utf8mb4_general_ci',
    cate1_nm VARCHAR(255) NOT NULL COMMENT '상권업종대분류명 ' COLLATE 'utf8mb4_general_ci',
    cate2_cd CHAR(4) NOT NULL COMMENT '상권업종중분류코드 ' COLLATE 'utf8mb4_general_ci',
    cate2_nm VARCHAR(255) NOT NULL COMMENT '상권업종중분류명 ' COLLATE 'utf8mb4_general_ci',
    cate3_cd CHAR(6) NOT NULL COMMENT '상권업종소분류코드 ' COLLATE 'utf8mb4_general_ci',
    cate3_nm VARCHAR(255) NOT NULL COMMENT '상권업종소분류명 ' COLLATE 'utf8mb4_general_ci',
    std_cd CHAR(6) NOT NULL COMMENT '표준산업분류코드 ' COLLATE 'utf8mb4_general_ci',
    std_nm VARCHAR(255) NOT NULL COMMENT '표준산업분류명 ' COLLATE 'utf8mb4_general_ci',
    addr1 VARCHAR(255) NOT NULL COMMENT '시도명 ' COLLATE 'utf8mb4_general_ci',
    addr2 VARCHAR(255) NOT NULL COMMENT '시군구명 ' COLLATE 'utf8mb4_general_ci',
    addr3 VARCHAR(255) NOT NULL COMMENT '행정동명 ' COLLATE 'utf8mb4_general_ci',
    addr4 VARCHAR(255) NOT NULL COMMENT '법정동명 ' COLLATE 'utf8mb4_general_ci',
    addr_num1 DECIMAL(4,0) NOT NULL COMMENT '지번본번지 ',
    addr_num2 DECIMAL(4,0) NOT NULL COMMENT '지번부번지 ',
    addr_bld VARCHAR(255) NOT NULL COMMENT '건물명 ' COLLATE 'utf8mb4_general_ci',
    floor_nm VARCHAR(10) NOT NULL COMMENT '층 위치' COLLATE 'utf8mb4_general_ci',
    lon DECIMAL(16,12) NOT NULL COMMENT '경도 ',
    lat DECIMAL(16,12) NOT NULL COMMENT '위도 ',
    PRIMARY KEY (seq_no) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=INNODB;


# addr3 단위로 가장 많은 상권소분류(cate3_cd or cate3_nm) 업종 중 가장 많은 기준으로 랭킹 1개씩 출력
WITH ranked AS (
    SELECT
        addr3,
        cate3_cd,
        cate3_nm,
        COUNT(*) AS cnt,
        ROW_NUMBER() OVER (PARTITION BY addr3 ORDER BY COUNT(*) DESC) AS rk
    FROM
        fact_smb_master
    GROUP BY
        addr3, cate3_cd, cate3_nm
)
SELECT
    addr3,
    cate3_cd,
    cate3_nm,
    cnt
FROM
    ranked
WHERE
    rk = 1
ORDER BY
    addr3;


# mart_smb_top_cate3에 데이터 붓기
INSERT INTO mart_smb_top_cate3 (addr3, cate3_cd, cate3_nm, cnt)
WITH ranked AS (
    SELECT
        addr3,
        cate3_cd,
        cate3_nm,
        COUNT(*) AS cnt,
        ROW_NUMBER() OVER (PARTITION BY addr3 ORDER BY COUNT(*) DESC) AS rn
    FROM fact_smb_master
    GROUP BY addr3, cate3_cd, cate3_nm
)
SELECT addr3, cate3_cd, cate3_nm, cnt
FROM ranked
WHERE rn = 1;











