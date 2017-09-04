-- Created on Fri Jul 28 15:35:00 2017
-- @author: TristanSong

CREATE DATABASE IF NOT EXISTS 2h_OEE;
USE 2h_OEE;
/*
-- 创建员工信息表
CREATE TABLE IF NOT EXISTS employee_db
(
	ic_card VARCHAR(10) NOT NULL PRIMARY KEY,
	employee_id VARCHAR(10) NOT NULL,
	name VARCHAR(20) NOT NULL,
	shift TINYINT NOT NULL,
	CONSTRAINT constraint_1 CHECK(shift>=0 AND shift<4)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
LOAD DATA LOCAL INFILE
'C:/Users/song-46/Desktop/2h_OEE/employee_db.csv'
REPLACE
INTO TABLE employee_db
CHARACTER SET UTF8
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r'
IGNORE 1 LINES;
*/

/*
CREATE TABLE IF NOT EXISTS cf_db
(
	id INT AUTO_INCREMENT PRIMARY KEY,
	bom VARCHAR(10) NOT NULL,
	cf VARCHAR(20) NOT NULL,
	cnc VARCHAR(10) NOT NULL DEFAULT '0#',
	shift_output SMALLINT NOT NULL,
	stand1 TINYINT NOT NULL, 
	stand2 TINYINT NOT NULL, 
	stand3 TINYINT NOT NULL,
	stand4 TINYINT NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
LOAD DATA LOCAL INFILE
'C:/Users/song-46/Desktop/2h_OEE/cf_db.csv'
REPLACE
INTO TABLE cf_db
CHARACTER SET UTF8
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r'
IGNORE 1 LINES
(bom, cf, cnc, shift_output, stand1, stand2, stand3, stand4);
*/


CREATE TABLE IF NOT EXISTS 6_db
(
	id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
	submit_time DATETIME NOT NULL DEFAULT NOW(),
	shift TINYINT NOT NULL, 
	CONSTRAINT constraint_1 CHECK(shift>0 AND shift<4),
	name VARCHAR(20) NOT NULL,
	duration TINYINT NOT NULL, 
	CONSTRAINT constraint_2 CHECK(duration>0 AND duration<13),
	cf VARCHAR(20) NOT NULL,
	cf_time FLOAT(4, 2) NOT NULL, 
	cf_stand TINYINT NOT NULL, 
	cf_output TINYINT NOT NULL, 
	cf_ok TINYINT NOT NULL,
	load_1 TINYINT NOT NULL, 
	changeover TINYINT NOT NULL,
	down TINYINT NOT NULL,
	temp TINYINT NOT NULL,
	no_order TINYINT NOT NULL, 
	mat_lack TINYINT NOT NULL,
	maintein TINYINT NOT NULL,
	other TINYINT NOT NULL,
	note VARCHAR(30),
	calendar_time TINYINT NOT NULL,
	plan_time TINYINT NOT NULL, 
	load_time TINYINT NOT NULL,
	utility FLOAT(5, 4) NOT NULL,
	ideal_time FLOAT(4, 1) NOT NULL,
	prototype TINYINT NOT NULL DEFAULT 0,
	availability FLOAT(5, 4) NOT NULL DEFAULT 0,
	performance FLOAT(5, 4) NOT NULL DEFAULT 0,
	quality FLOAT(5, 4) NOT NULL DEFAULT 0,
	oee_shift FLOAT(5, 4) NOT NULL DEFAULT 0,
	teep_shift FLOAT(5, 4) NOT NULL DEFAULT 0,
	oee_day FLOAT(5, 4) NOT NULL DEFAULT 0,
	teep_day FLOAT(5, 4) NOT NULL DEFAULT 0
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;