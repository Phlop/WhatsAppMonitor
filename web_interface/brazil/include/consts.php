<?php
/**
 * Hard coded constants
 *
 * @author Johnnatan Messias <johnme@mpi-sws.org>
 */

define("DSN_whatsapp", 'pgsql:host=127.0.0.1;dbname=whatsapp;'
    . 'user=*****;password=**********'
    . 'connect_timeout=10');

define('DSN_MAIN', DSN_whatsapp);

define('MAX_IMAGES', 30);

//1 week = 604800s = 7 * 24 * 60 * 60
define('CACHE_VALID', 604800);

//define('CACHE_VALID', 1);
