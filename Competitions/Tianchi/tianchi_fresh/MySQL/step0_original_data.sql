-- mysql
-- ***********************************
-- created on Mon May 15 23:30:00 2017
-- @author:TristanSong
-- ***********************************


DROP DATABASE IF EXISTS TIANCHI_FRESH;
CREATE DATABASE TIANCHI_FRESH;
USE TIANCHI_FRESH;

-- 导入用户历史行为记录
DROP TABLE IF EXISTS Train_User;
CREATE TABLE Train_User
(
	user_id VARCHAR(10) NOT NULL,
    item_id VARCHAR(10) NOT NULL,
    behavior_type INT1 NOT NULL CHECK(behavior_type LIKE '[1234]'),
    user_geohash VARCHAR(10),
    item_category BIGINT(5) NOT NULL,
    change_time TIMESTAMP NOT NULL 
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
LOAD DATA LOCAL INFILE 
"/Volumes/macOS_HD/Python/TianChi/tianchi_fresh/tianchi_fresh_comp_train_user.csv"
REPLACE
INTO TABLE Train_User
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

ALTER TABLE Train_User
ADD INDEX change_date (change_time);

ALTER TABLE Train_User
ADD INDEX b_type (behavior_type);


-- 导入商品子集
DROP TABLE IF EXISTS Train_Item;
CREATE TABLE Train_Item
(
	item_id VARCHAR(10) NOT NULL,
    item_geohash VARCHAR(10),
    item_category BIGINT(10) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
LOAD DATA LOCAL INFILE
"/Volumes/macOS_HD/Python/TianChi/tianchi_fresh/tianchi_fresh_comp_train_item.csv"
REPLACE
INTO TABLE Train_Item
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;