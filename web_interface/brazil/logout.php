<?php
/**
 * The user logout page
 *
 * @author Johnnatan Messias <johnme@mpi-sws.org>
 */


require_once 'include/init.php';
ob_start();
if (session_status() == PHP_SESSION_NONE) {
  session_start();
}
session_regenerate_id();
session_unset();
session_destroy();

header('Location: ./index.php');

// Don't close the PHP tag
