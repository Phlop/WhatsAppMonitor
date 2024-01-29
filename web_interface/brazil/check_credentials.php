<?php

require_once("include/init.php");
require_once("main.php");

$email = trim(get_default($_POST, 'inputEmail', ''));
$passwd = trim(get_default($_POST, 'inputPassword', ''));

try{
        $db = db_connect(DSN_MAIN);
}catch (Exception $e){
    header("HTTP/1.1 303 See Other");
    header("Location: ./index.php");
}

if(is_user_registered($db, $email, $passwd) === true){

  $interval = new DateInterval('P1D');
  $_SESSION['user'] = get_user_personal_data($db, $email);
  $previous_date = new DateTime(date("Y-m-d"));
  $previous_date->sub($interval);
  
  $last_upd_date = get_last_update_date($db);
  if (!isset($last_upd_date)){
    $last_upd_date[0] = $previous_date->format('Y-m-d');
  }

  $_SESSION['last_upd_date'] = $last_upd_date[0];
  $_SESSION['user_logged'] = true;
  //header("Location: ./app.php?flag=images&end_date=2019-01-01&obtained_at=". $previous_date->format('Y-m-d'));
  header("Location: ./app.php?flag=images&end_date=". $last_upd_date[0]. "&obtained_at=". $last_upd_date[0]);
  exit();
}else{
    header("HTTP/1.1 303 See Other");
    header("Location: ./login.php?ecode=not_found_user");
    exit();
}

?>
