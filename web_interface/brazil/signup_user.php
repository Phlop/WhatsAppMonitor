<?php

require_once("include/init.php");
require_once("main.php");

if (!isset($_SESSION['user_logged'])) {
  header("HTTP/1.1 303 See Other");
  header("Location: ./login.php?ecode=not_logged_in");
  exit();
}

if ($_SESSION['user']['superuser'] === false){
  header("Location: ./index.php");
  exit();
}

$email = trim(get_default($_POST, 'email', ''));
$passwd = trim(get_default($_POST, 'psw', ''));

$fname = trim(get_default($_POST, 'first-name', ''));
$lname = trim(get_default($_POST, 'last-name', ''));
$company = trim(get_default($_POST, 'company', ''));
$superuser = trim(get_default($_POST, 'superuser', 'FALSE'));

if ($email === ''){
  header("Location: ./index.php");
  exit();
}


try{
        $db = db_connect(DSN_MAIN);
}catch (Exception $e){
    header("HTTP/1.1 303 See Other");
    header("Location: ./login.php");
}

if(!is_email_registered($db, $email, $passwd) === true){
  if(!insert_user($db, $email, $passwd, $fname, $lname, $company, $superuser)){
    header("Location: ./signup.php?ecode=error_registered_user");
  }
  header("Location: ./signup.php?ecode=user_registered");
  exit();
}else{
    header("HTTP/1.1 303 See Other");
    header("Location: ./signup.php?ecode=user_already_registered");
    exit();
}

?>
