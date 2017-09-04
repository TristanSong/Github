-- mysql
-- ***********************************
-- created on Wed May 16 14:22:00 2017
-- @author:TristanSong
-- ***********************************

/*
SELECT precision, recall, 2*precision*recall/(precision+recall) AS F1
FROM
(
	SELECT	SUM(IF(!ISNULL(A.item_id) AND !ISNULL(B.item_id), 1, 0))/SUM(!ISNULL(A.item_id, 1, 0)) AS precision,
			SUM(IF(!ISNULL(A.item_id) AND !ISNULL(B.item_id), 1, 0))/SUM(!ISNULL(B.item_id, 1, 0)) AS recall
	FROM Rule_1 AS A
	FULL OUTER JOIN Data_Test AS B
	ON A.user_id=B.user_id AND A.item_id=B.item_id
)C;
*/

SELECT SUM(IF(!ISNULL(B.item_id), 1, 0)) AS d1, COUNT(*) AS d2
FROM Predict AS A
LEFT OUTER JOIN Data_Test AS B 
ON A.user_id=B.user_id AND A.item_id=B.item_id;

SELECT SUM(IF(!ISNULL(A.item_id), 1, 0)) AS d1, COUNT(*) AS d2
FROM Predict AS A
RIGHT OUTER JOIN Data_Test AS B 
ON A.user_id=B.user_id AND A.item_id=B.item_id;