CREATE TABLE mart_smb_top_cate3 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    addr3 VARCHAR(255) NOT NULL COMMENT '행정동명',
    cate3_cd CHAR(6) NOT NULL COMMENT '상권업종소분류코드',
    cate3_nm VARCHAR(255) NOT NULL COMMENT '상권업종소분류명',
    cnt INT NOT NULL COMMENT '해당 업종 점포수',
    UNIQUE KEY uniq_addr3_cate3 (addr3, cate3_cd)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=UTF8MB4_GENERAL_CI;
