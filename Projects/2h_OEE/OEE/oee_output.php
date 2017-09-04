<?php
header("Content-type=text/json, charset=UTF-8");
date_default_timezone_set('prc');
$Y = date('Y', time());
$m = date('m', time());
$d = date('d', time());
$hour = date('H', time());
if ($hour<8){
	$time0 = date('Y-m-d H:i:s', mktime(0, 0, 0, $m, $d, $Y));
	$time1 = date('Y-m-d H:i:s', mktime(8, 0, 0, $m, $d, $Y));
} elseif ($hour<16){
	$time0 = date('Y-m-d H:i:s', mktime(8, 0, 0, $m, $d, $Y));
	$time1 = date('Y-m-d H:i:s', mktime(16, 0, 0, $m, $d, $Y));
} else{
	$time0 = date('Y-m-d H:i:s', mktime(16, 0, 0, $m, $d, $Y));
	$time1 = date('Y-m-d H:i:s', mktime(23, 59, 59, $m, $d, $Y));
}

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

$data = array();
class cf_output{
	public $cf_total;
	public $cf_output;
}

foreach($cnc_names as $cnc){
	$results_1 = mysqli_query($conn, "SELECT cf_time FROM {$cnc} WHERE submit_time>='{$time0}' AND submit_time<'{$time1}' LIMIT 1");
	$results_2 = mysqli_query($conn, "SELECT cf_output FROM {$cnc} WHERE submit_time>='{$time0}' AND submit_time<'{$time1}'");
	//处理数据
	$cf = new cf_output();
	//取得标准产量
	$value_1 = mysqli_fetch_array($results_1, MYSQLI_ASSOC);
	if (empty($value_1)){
		$cf->cf_total = 0;
	}else{
		$cf->cf_total = 420/$value_1['cf_time'];
	}
	//取得累计产量
	$value_2 = 0;
	while ($row = mysqli_fetch_array($results_2, MYSQLI_ASSOC)){
		$value_2 += $row['cf_output'];
	}
	$cf->cf_output = $value_2;
	$data[] = $cf;
}

mysqli_close($conn);
//返回json数据
echo json_encode($data);
?>