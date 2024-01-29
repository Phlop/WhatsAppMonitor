<?php
ini_set('session.gc_maxlifetime', 7200);
session_name("monitor-de-whatsapp");
// each client should remember their session id for EXACTLY 1 hour
session_set_cookie_params(7200);

session_start();
?>

<?php
/**
 * Include this in all public facing PHP codes
 *
 * @author Johnnatan Messias <johnme@mpi-sws.org>
 */

error_reporting(-1);
/* error_reporting(0); */
ini_set('display_errors', 'stdout');
ini_set('html_errors', 1);
setlocale(LC_ALL, 'pt_BR');
setlocale(LC_TIME, 'pt_BR', 'pt_BR.utf-8', 'pt_BR.utf-8', 'portuguese');

// Include the general libraries
require_once 'consts.php';
require_once 'utilities.php';
require_once 'db.php';

// Do this otherwise we block the entire PHP server
// This brings $_SESSION in scope

//session_register();
//session_start();

//session_write_close();

// Don't close the PHP tag
