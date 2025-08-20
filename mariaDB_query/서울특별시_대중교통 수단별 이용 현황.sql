CREATE TABLE tb_subway (
    t_type VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    t_num VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    t_date VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    t_count VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    d_count BIGINT(20) NULL DEFAULT NULL
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;

UPDATE tb_subway
SET d_count = convert(t_count, INTEGER);

# 지하철 1호선의 2018년도 전체 이용자수를 구하시오
SELECT SUM(d_count) AS cnt
FROM tb_subway
WHERE t_num = '1호선'
AND t_date LIKE '2018%';

# 2018년도 지하철 각 호선별로 가장 이용자가 많은 월을 출력하시오
SELECT t_num, t_date, d_count
FROM(
SELECT t_num, t_date, d_count
, RANK() OVER (PARTITION BY t_num ORDER BY d_count DESC) AS t_rank
FROM tb_subway
WHERE t_date LIKE '2018%'
) temp_ranked
WHERE t_rank = 1;

# 2018년도 지하철 각 호선별로 가장 이용자가 적은 월을 출력하시오.
SELECT t_num, t_date, d_count
FROM(
SELECT t_num, t_date, d_count
, RANK() OVER (PARTITION BY t_num ORDER BY d_count) AS t_rank
FROM tb_subway
WHERE t_date LIKE '2018%'
) temp_ranked
WHERE t_rank = 1;



