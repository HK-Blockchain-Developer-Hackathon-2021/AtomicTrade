<?php 


if ( 0 < $_FILES['file']['error'] ) {
    echo 'Error: ' . $_FILES['file']['error'] . '<br>';
}
else {
    $filename= $_FILES['file']['name'] ; 
    move_uploaded_file($_FILES['file']['tmp_name'], $filename);
    $str_output = exec ("python web_scrapping.py /$filename" );
    echo ($str_output);
}


?>