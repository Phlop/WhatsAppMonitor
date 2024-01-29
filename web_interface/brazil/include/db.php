<?php
/**
 * Convinence methods for making database queries
 *
 * @author Parantapa Bhattacharya <pb@parantapa.net>
 */

// Connect to the database using PDO
function db_connect($dsn, $db = null)
{
    // Do not reconnect it connection is already there
    if ($db !== null) {
        return $db;
    }

    // Try to connect
    try {
        $db = new PDO($dsn);
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    } catch (PDOException $e) {
        throw new Exception();
        die('Could not connect: ' . $e->getMessage());
    }

    // return the connection object
    return $db;
}

// Short function for quering using PDO
function db_query($db, $query)
{
    if (func_num_args() == 2) {
        try {
            $sth = $db->query($query);
        } catch (PDOException $e) {
            die('Query failed: ' . $e->getMessage());
        }
        return $sth;
    }

    $args = func_get_args();
    $params = array_splice($args, 2);
    try {
        $sth = $db->prepare($query);
        $sth->execute($params);
    } catch (PDOException $e) {
        debug_print_backtrace();
        die('Query failed: ' . $e->getMessage());
    }
    return $sth;
}

function db_query_optmized($db, $query)
{
    //make the query here
    try {
        $sth = $db->prepare($query);
        $sth->execute();
    } catch (PDOException $e) {
        debug_print_backtrace();
        die('Query failed: ' . $e->getMessage());
    }
    return $sth;
}

// Don't close the PHP tag
