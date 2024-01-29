<?php
/**
 * Misc utility functions
 *
 * @author Parantapa Bhattacharya <pb@parantapa.net>
 */

// Get value from array or default if not available
function get_default($arr, $key, $default)
{
    if (array_key_exists($key, $arr)) {
        return $arr[$key];
    }

    return $default;
}

// Equevalent of python dict.items()
function assoc_items($assoc)
{
    $ret = array();
    foreach ($assoc as $k => $v) {
        $ret[] = array($k, $v);
    }
    return $ret;
}

// Increment a value in an array
// If value not already there assume to be zero
function incr_default(&$arr, $key)
{
    if (array_key_exists($key, $arr)) {
        $arr[$key] += 1;
    } else {
        $arr[$key] = 1;
    }
}

// Return url in the current server
// Stolen from:
// https://stackoverflow.com/questions/2820723/how-to-get-base-url-with-php
function make_url($url)
{
    $proto = isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] != 'off' ? 'https' : 'http';
    return sprintf("%s://%s%s", $proto, $_SERVER['HTTP_HOST'], $url);
}

// Don't close the PHP tag
