<?php
header("Content-type=text/json, charset=UTF-8");
//连接MariaDB数据库
$conn = mysqli_connect("localhost","root","") or die("Connection failed!");
mysqli_query($conn, "set names utf-8");
mysqli_select_db($conn, "2h_OEE");

//获取所有机床数据库的名称
$results_0 = mysqli_query($conn, "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='2h_OEE'");
$cnc_names = array();
while ($row = mysqli_fetch_array($results_0, MYSQLI_ASSOC)){
	if (preg_match("/^\d/", $row['TABLE_NAME'])){
		$cnc_names[] = $row['TABLE_NAME'];
	}
}
sort($cnc_names);

//根据机床数据库提取数据
$data = array();
class User{
	public $oee_day;
	public $teep_day;
}

foreach ($cnc_names as $cnc){
	$results_1 = mysqli_query($conn, "SELECT oee_day, teep_day FROM {$cnc} WHERE submit_time<NOW() AND oee_day != 0 ORDER BY submit_time DESC LIMIT 1");
	while ($row = mysqli_fetch_array($results_1, MYSQLI_ASSOC)){
		$user = new User();
		$user->oee_day = $row['oee_day'];
		$user->teep_day = $row['teep_day'];
		$data[] = $user;
	}
}

mysqli_close($conn);
//返回json数据
echo json_encode($data);
?>