<?php
header("Content-type=text/json, charset=UTF-8");
//连接MariaDB数据库
$conn = mysqli_connect("localhost","root","") or die("Connection failed!");
mysqli_query($conn, "set names utf-8");
mysqli_select_db($conn, "2h_OEE");

//获取所有机床数据库的名称
$results = mysqli_query($conn, "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='2h_OEE'");

$cnc_names = array();

while ($row = mysqli_fetch_array($results, MYSQLI_ASSOC)){
	if (preg_match("/^\d/", $row['TABLE_NAME'])){
		$cnc_names[] = str_replace("_db", "#", $row["TABLE_NAME"]);
	}
}

sort($cnc_names);

mysqli_close($conn);
echo json_encode($cnc_names);
?>