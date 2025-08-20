CREATE TABLE mart_weather_aws_hour (
    yyyymmddhh CHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    stn_id CHAR(4) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    stn_ko VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    ta_min DECIMAL(6,2) NULL DEFAULT NULL,
    ta_max DECIMAL(6,2) NULL DEFAULT NULL
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;


INSERT INTO mart_weather_aws_hour
(yyyymmddhh, stn_id, stn_ko, ta_min, ta_max)
SELECT SUBSTRING(yyyymmddhhmi, 1, 10) AS yyyymmddhh
, stn AS stn_id
, (SELECT STN_KO FROM tb_weather_tcn t WHERE t.STN_ID = stn) AS stn_ko
, MIN(ta) AS ta_min
, MAX(ta) AS ta_max
FROM fact_weather_aws1
WHERE ta > -90.0
GROUP BY yyyymmddhh, stn_id

