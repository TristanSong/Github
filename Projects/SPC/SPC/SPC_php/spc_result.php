<?php
header("Content-type=text/json, charset=UTF-8");
//连接MariaDB数据库
$conn = mysqli_connect("localhost","root","") or die("Connection failed!");
mysqli_query($conn, "set names utf-8");
mysqli_select_db($conn, "nova_spc");

//从前台ajax接收，用于指定具体提取数据库数据
//$name = '500g_38';
//$num = 100;
$name = $_POST['name'];
$num = $_POST['num'];
//根据机床数据库提取数据
$data = array();
class cnc_data{
	public $M_TIME;
	public $L_UP;
	public $L_MID;
	public $L_D;
	public $UCL;
	public $LCL;
	public $AVE;
	public $DIFF;
	public $AVE_EACH;
}

$length = 0;
$t = array();
$arr = array();
//每组数据均值
$aves = array();
//每组数据极差
$diffs = array();
$results_1 = mysqli_query($conn, "SELECT m_time, t1, t2, t3, t4, t5, t6, t7, t8 FROM {$name} WHERE m_time<NOW() ORDER BY m_time LIMIT {$num}");
while ($row = mysqli_fetch_array($results_1, MYSQLI_ASSOC)){
	$t[] = $row['m_time'];
	$length += 1;
	$arr[] = $row['t1'];
	$arr[] = $row['t2'];
	$arr[] = $row['t3'];
	$arr[] = $row['t4'];
	$arr[] = $row['t5'];
	$arr[] = $row['t6'];
	$arr[] = $row['t7'];
	$arr[] = $row['t8'];
	
	$temp_array = array();
	$temp_array[] = $row['t1'];
	$temp_array[] = $row['t2'];
	$temp_array[] = $row['t3'];
	$temp_array[] = $row['t4'];
	$temp_array[] = $row['t5'];
	$temp_array[] = $row['t6'];
	$temp_array[] = $row['t7'];
	$temp_array[] = $row['t8'];
	//sprintf用于将float数据进行四舍五入
	$aves[] = sprintf("%.3f", array_sum($temp_array)/8);
	$diffs[] = sprintf("%.3f", (max($temp_array) - min($temp_array)));
}
//总均值
$average = sprintf("%.3f", array_sum($arr)/$length/8);
$count = 0;
foreach ($arr as $a){
	$count += pow($average-$a, 2);
}
//总标准差
$sigma = sprintf("%.4f", sqrt($count/$length));

//每组数据公差上线、公差中限、公差下限、控制上限、控制下限、总均值
$ups = array();
$mids = array();
$downs = array();
$ucls = array();
$lcls = array();
$averages = array();
//NOVA 5kg	
if (strstr($name, "5kg")){
	for ($i=0; $i<$length; $i++){
		$ups[] = 0.530;
		$mids[] = 0.500;
		$downs[] = 0.470;
		$ucls[] = sprintf("%.3f", 0.500 + 1*$sigma);
		$lcls[] = sprintf("%.3f", 0.500 - 1*$sigma);
		$averages[] = $average;
	}
}
//NOVA 500g
elseif (strstr($name, "500g")){
	for ($i=0; $i<$length; $i++){
		$ups[] = 0.330;
		$mids[] = 0.300;
		$downs[] = 0.270;
		$ucls[] = sprintf("%.3f", 0.300 + 3*$sigma);
		$lcls[] = sprintf("%.3f", 0.300 - 3*$sigma);
		$averages[] = $average;
	}
}
//NOVA 300g
else{
	for ($i=0; $i<$length; $i++){
		$ups[] = 0.830;
		$mids[] = 0.800;
		$downs[] = 0.770;
		$ucls[] = sprintf("%.3f", 0.800 + 3*$sigma);
		$lcls[] = sprintf("%.3f", 0.800 - 3*$sigma);
		$averages[] = $average;
	}
}
//机床数据存入总data
$d = new cnc_data();
$d->M_TIME = $t;
$d->L_UP = $ups;
$d->L_MID = $mids;
$d->L_D = $downs;
$d->UCL = $ucls;
$d->LCL = $lcls;
$d->AVE = $averages;
$d->DIFF = $diffs;
$d->AVE_EACH = $aves;
$data[]=$d;


mysqli_close($conn);
//返回json数据
//echo json_encode($sigma);
echo json_encode($data);
?>