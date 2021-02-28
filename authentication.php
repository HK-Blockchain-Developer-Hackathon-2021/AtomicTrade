<?php

    session_start();
    if(isset($_GET['action']) && $_GET['action'] == 'logout')
	{
		session_destroy();
		$_SESSION = array();
		//echo ($_SESSION['user']);
		header("Location: index.php");
	}else if($_POST)
	{
		$_SESSION['loggedIn'] = time();
		$_SESSION['user'] = $_POST['address'];
		$_SESSION['passphrase'] = $_POST['passphrase'];
		echo("success");
		
		
	}
?>
