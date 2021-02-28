<?php

//$output = shell_exec('rm *.html');
//echo $output;
ini_set('memory_limit','256M');
$data=  $_POST['data'];

$data = json_encode($data,JSON_UNESCAPED_SLASHES);
$str_output = exec ("python main.py .$data" );
//$str_output = exec ( "$Path $var1" );
echo $str_output;


/*html_file=""
html_file+=sys.argv[1]
txn_type = html_file[1:] #get txn type from user input
*/
?>