CREATE TABLE `tb_smb_ods` (
	`col1` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col2` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col3` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col4` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col5` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col6` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col7` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col8` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col9` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col10` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col11` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col12` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col13` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col14` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col15` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col16` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col17` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col18` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col19` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col20` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col21` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col22` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col23` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col24` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col25` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col26` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col27` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col28` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col29` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col30` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col31` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col32` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col33` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col34` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col35` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col36` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col37` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col38` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`col39` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci'
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;
 

SET GLOBAL local_infile = 1; 


INSERT INTO fact_smb_master 
(smb_id, smb_name, smb_subnm, cate1_cd, cate1_nm, cate2_cd, cate2_nm, cate3_cd, cate3_nm, std_cd, std_nm, addr1, addr2, addr3, addr4, addr_num1, addr_num2, addr_bld, floor_nm, lon, lat)
SELECT col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col13, col15, col17, col19, convert(col23, DECIMAL(4)), convert(col24, DECIMAL(4)), col26, col36, convert(col38, DECIMAL(16,12)), convert(col39, DECIMAL(16,12))
FROM tb_smb_ods;fact_smb_master
     