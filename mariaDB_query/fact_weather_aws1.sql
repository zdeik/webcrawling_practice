CREATE TABLE fact_weather_aws1 (
    seq_no BIGINT(20) NOT NULL AUTO_INCREMENT,
    yyyymmddhhmi CHAR(12) NOT NULL DEFAULT '0' COLLATE 'utf8mb4_general_ci',
    stn CHAR(4) NOT NULL DEFAULT '0' COLLATE 'utf8mb4_general_ci',
    wd1 DECIMAL(6,1) NOT NULL DEFAULT '0.0',
    ws1 DECIMAL(6,1) NOT NULL DEFAULT '0.0',
    wds DECIMAL(6,1) NOT NULL DEFAULT '0.0',
    wss DECIMAL(6,1) NOT NULL DEFAULT '0.0',
    wd10 DECIMAL(6,1) NOT NULL DEFAULT '0.0',
    ws10 DECIMAL(6,1) NOT NULL DEFAULT '0.0',
    ta DECIMAL(6,1) NOT NULL DEFAULT '0.0',
    re DECIMAL(6,1) NOT NULL DEFAULT '0.0',
    rn_15m DECIMAL(6,1) NOT NULL DEFAULT '0.0',
    rn_60m DECIMAL(6,1) NOT NULL DEFAULT '0.0',
    rn_12h DECIMAL(6,1) NOT NULL DEFAULT '0.0',
    rn_day DECIMAL(6,1) NOT NULL DEFAULT '0.0',
    hm DECIMAL(6,1) NOT NULL DEFAULT '0.0',
    pa DECIMAL(6,1) NOT NULL DEFAULT '0.0',
    ps DECIMAL(6,1) NOT NULL DEFAULT '0.0',
    td DECIMAL(6,1) NOT NULL DEFAULT '0.0',
    update_dt CHAR(50) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
    PRIMARY KEY (seq_no) USING BTREE,
    INDEX yyyymmddhhmi_stn (yyyymmddhhmi, stn) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;

INSERT INTO fact_weather_aws1(yyyymmddhhmi, stn, wd1, ws1, wds, wss, wd10, ws10, ta, re, rn_15m, rn_60m, rn_12h, rn_day, hm, pa, ps, td, UPDATE_dt )
SELECT yyyymmddhhmi, stn
, convert(wd1, DECIMAL(6,2))
, convert(ws1, DECIMAL(6,2))
, convert(wds, DECIMAL(6,2))
, convert(wss, DECIMAL(6,2))
, convert(wd10, DECIMAL(6,2))
, convert(ws10, DECIMAL(6,2))
, convert(ta, DECIMAL(6,2))
, if ( convert(re, DECIMAL(6,2)) < 0, 0.0, convert(re, DECIMAL(6,2)) )
, if ( convert(rn_15m, DECIMAL(6,2)) < 0, 0.0, convert(rn_15m, DECIMAL(6,2)) )
, if ( convert(rn_60m, DECIMAL(6,2)) < 0, 0.0, convert(rn_60m, DECIMAL(6,2)) )
, if ( convert(rn_12h, DECIMAL(6,2)) < 0, 0.0, convert(rn_12h, DECIMAL(6,2)) )
, if ( convert(rn_day, DECIMAL(6,2)) < 0, 0.0, convert(rn_day, DECIMAL(6,2)) )
, convert(hm, DECIMAL(6,2))
, convert(pa, DECIMAL(6,2))
, convert(ps, DECIMAL(6,2))
, convert(td, DECIMAL(6,2))
, NOW()
FROM tb_weather_aws1
