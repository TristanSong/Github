-- mysql
-- ***********************************
-- created on Tue May 15 08:54:00 2017
-- @author:TristanSong
-- ***********************************

USE TIANCHI_FRESH;

-- 训练集
DROP TABLE IF EXISTS Data_Train;
CREATE TABLE Data_Train AS
SELECT *
FROM Train_User
WHERE change_time<TIMESTAMP('2014-12-18 00');
/*
-- 效率太低，慢了一倍多
DROP TABLE IF EXISTS Data_Train;
CREATE TABLE Data_Train
(
	user_id VARCHAR(10) NOT NULL,
    item_id VARCHAR(10) NOT NULL,
    behavior_type INT1 NOT NULL CHECK(behavior_type LIKE '[1234]'),
    user_geohash VARCHAR(10),
    item_category BIGINT(5) NOT NULL,
    change_time TIMESTAMP NOT NULL 
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO Data_Train
(
	user_id,
    item_id,
    behavior_type,
    user_geohash,
    item_category,
    change_time
)
SELECT DISTINCT *
FROM Train_User
AS Data_Train
WHERE change_time<TIMESTAMP('2014-12-18 00');
*/


-- 测试集
USE TIANCHI_FRESH;
DROP TABLE IF EXISTS Data_Test;
CREATE TABLE Data_Test AS
SELECT A.user_id, A.item_id
FROM
(
	SELECT user_id, item_id
	FROM Train_User
	WHERE change_time>=TIMESTAMP('2014-12-18 00') AND behavior_type=4
	GROUP BY user_id, item_id
)AS A
LEFT OUTER JOIN Train_Item AS B
ON A.item_id = B.item_id
WHERE !ISNULL(B.item_id)
GROUP BY A.user_id, A.item_id;