<?php
header("Content-type=text/json, charset=UTF-8");
//连接MariaDB数据库
$conn = mysqli_connect("localhost","root","") or die("Connection failed!");
mysqli_query($conn, "set names utf-8");
mysqli_select_db($conn, "nova_spc");

//获取所有机床数据库的名称
$results = mysqli_query($conn, "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='nova_spc'");

$names = array();

while ($row = mysqli_fetch_array($results, MYSQLI_ASSOC)){
	$names[] = $row["TABLE_NAME"];
}

sort($names);

mysqli_close($conn);
echo json_encode($names);
?>