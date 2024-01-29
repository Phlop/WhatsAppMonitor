<?php
/**
 * The user search page
 *
 * @author Johnnatan Messias <johnme@mpi-sws.org>
 */

require_once 'include/utilities.php';
require_once 'include/consts.php';

$op = get_default($_POST, 'op', -1);
$obtained_at = get_default($_POST, 'date', '');
$end_date = get_default($_POST, 'end_date', '');
$offset = get_default($_POST, 'offset', 0);

$email = get_default($_POST, 'email', '');
$imageid = get_default($_POST, 'imageid', '');
$tags = get_default($_POST, 'tags', '');
$comments = get_default($_POST, 'comments', '');
$type = get_default($_POST, 'type', 'image');


if ($op == 1010){
	$json_data = sprintf('{"op": %s, "obtained_at": "%s", "end_date": "%s", "offset": %s, "type":"%s"}', $op, date("Y-m-d", strtotime($obtained_at)), date("Y-m-d", strtotime($end_date)), $offset, $type);
}else if ($op == 102312){
	$json_data = sprintf('{"op": %s, "email": "%s", "imageid": "%s", "tags": %s, "comments": "%s", "type":"%s"}', $op, $email, $imageid, $tags, $comments, $type);
}


//$fp = fopen('W_SAIDA.txt', 'w');
//fwrite($fp, $json_data);
//fclose($fp);

$cmd = sprintf("python2 kernel.py '%s'", $json_data);
$out = shell_exec($cmd);
echo $out;

?>
