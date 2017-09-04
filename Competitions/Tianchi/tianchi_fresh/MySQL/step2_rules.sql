-- mysql
-- ***********************************
-- created on Tue May 15 14:22:00 2017
-- @author:TristanSong
-- ***********************************

USE TIANCHI_FRESH;

-- 规则1: 最近购物车原则，当天加入购物车，第二天购买
-- 优化1: 用户当天已购买，第二天不买
-- 优化2：用户下半天加入购物车，第二天更有可能购买
DROP TABLE IF EXISTS Rule_1;
CREATE TABLE Rule_1 AS
SELECT C.user_id, C.item_id
FROM
(
	SELECT A.user_id, A.item_id
	FROM
    (
		-- 挑选下半天加入购物车
		SELECT user_id, item_id
        FROM Data_Train
		WHERE change_time>=TIMESTAMP('2014-12-17 12') 
        AND change_time<TIMESTAMP('2014-12-18 00') 
        AND behavior_type=3
		GROUP BY user_id, item_id
	)AS A
	LEFT OUTER JOIN
	(
		-- 挑选下半天已经购买
		SELECT user_id, item_id
		FROM Data_Train
		WHERE change_time>=TIMESTAMP('2014-12-17 12') 
        AND change_time<TIMESTAMP('2014-12-18 00') 
        AND behavior_type=4
		GROUP BY user_id, item_id
	)AS B
	ON A.user_id=B.user_id AND A.item_id=B.item_id
	WHERE ISNULL(B.item_id)
    -- 关键在于WHERE ISNULL(B.item_id)
	-- A LEFT OUTER JOIN B不仅返回符合联结条件的结果，还返回A中不符合联结条件的结果
    -- 符合联结条件的结果为：已加入购物车，并购买
    -- A中不符合联结条件的结果，为已加入购物车但未购买
    -- 实现A,B的差集{x∣x∈A,且x!∈B}
    -- ****************************************************************************
    -- WHERE !ISNULL(B.item_id)
    -- 实现A, B的交集
)AS C
LEFT OUTER JOIN Train_Item AS D
ON C.item_id=D.item_id
WHERE !ISNULL(D.item_id)
GROUP BY C.user_id, C.item_id;



-- 规则2:在规则1基础上，增加看了8遍以上没买的
DROP TABLE IF EXISTS Rule_2;
CREATE TABLE Rule_2 AS
SELECT A.user_id, A.item_id
FROM
(
	SELECT user_id, item_id
	FROM Data_Train
	WHERE change_time>=TIMESTAMP('2014-12-17 00')
	AND change_time<TIMESTAMP('2014-12-18 00')
	AND behavior_type=1
	GROUP BY user_id, item_id
	HAVING COUNT(*)>=10
)AS A
LEFT OUTER JOIN
(
	SELECT user_id, item_id
    FROM Data_Train
	WHERE change_time>=TIMESTAMP('2014-12-17 00')
	AND change_time<TIMESTAMP('2014-12-18 00')
	AND behavior_type=4
    GROUP BY user_id, item_id
)AS B
ON A.item_id=B.item_id AND A.user_id=B.user_id
WHERE ISNULL(B.user_id)
GROUP BY A.user_id, A.item_id;


/*
-- 规则理解错误
DROP TABLE IF EXISTS Rule_2;
CREATE TABLE Rule_2 AS
SELECT A.user_id, A.item_id
FROM Rule_1 AS A
LEFT OUTER JOIN
(
	SELECT user_id, item_id
	FROM Data_Train
	WHERE change_time>=TIMESTAMP('2014-12-17 00')
	AND change_time<TIMESTAMP('2014-12-18 00')
	AND behavior_type=1
	GROUP BY user_id, item_id
	HAVING COUNT(*)>=8
)AS B
ON A.user_id=B.user_id AND A.item_id=B.item_id
WHERE ISNULL(B.user_id)
GROUP BY A.user_id, A.item_id;
*/


-- 规则3：去除“加入多件商品进入购物车，但当天却仅支付个别商品”
DROP TABLE IF EXISTS Rule_3;
CREATE TABLE Rule_3 AS
SELECT A.user_id
FROM 
(
	SELECT user_id, count(user_id) AS add_times
	FROM Data_Train
	WHERE change_time>=TIMESTAMP('2014-12-17 00')
	AND change_time<TIMESTAMP('2014-12-18 00')
	AND behavior_type=3
	GROUP BY user_id, item_id
	HAVING COUNT(user_id)>1
)AS A
INNER JOIN
(
	SELECT user_id, count(user_id) AS buy_times
	FROM Data_Train
	WHERE change_time>=TIMESTAMP('2014-12-17 00')
	AND change_time<TIMESTAMP('2014-12-18 00')
	AND behavior_type=4
	GROUP BY user_id, item_id
)AS B
ON A.user_id=B.user_id
WHERE A.add_times>B.buy_times
GROUP BY A.user_id;



-- 规则合并
DROP TABLE IF EXISTS Predict;
CREATE TABLE Predict AS
SELECT A.user_id, A.item_id
FROM
(
	SELECT * FROM Rule_1
    UNION
    SELECT * FROM Rule_2
)AS A;

SET SQL_SAFE_UPDATES = 0;

DELETE FROM Predict 
USING Predict, Rule_3
WHERE Predict.user_id=Rule_3.user_id;

SET SQL_SAFE_UPDATES = 1;



-- 导出CSV
SELECT *
FROM Predict
INTO OUTFILE '/Volumes/macOS_HD/Python/TianChi/tianchi_fresh/MySQL/tianchi_mobile_recommendation_predict.csv'
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n';
