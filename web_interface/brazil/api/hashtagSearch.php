<?php
require_once '../include/consts.php';
require_once '../include/db.php';
require_once '../main.php';

$db = db_connect(DSN_MAIN);

$query = "";

if(isset($_GET['query'])) {
	$query = $_GET['query'];
}

if($query == "IWantMyHashtagsBackNowByJohnnataMessiasJustDoItNow007New__Br__"){
	print "<!DOCTYPE html>
<html>
<script src='../js/sorttable.js'></script>
<head>
<style>
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

tr:nth-child(even) {
    background-color: #dddddd;
}
</style>
</head>
<body>
";
	$hashtags = get_all_hashtags($db);
    echo "<table class='db-table'>";
    echo "<tr colspan='". $col_cnt ."'>". $tbl_name ."</tr>";
    echo "<tr>";

    echo '<h3>Twitter Trending Topics: Easter Egg by <a href="http://johnnatan.me">Johnnatan Messias</a></h3>';
    //echo '<h3>Default initial sort: (1st) #Trend_Date; (2nd) #Total_with_Dem_Info; (3rd) Hashtag</h3>';
    echo '<h3>Click on column names to sort';
	echo '<table cellpadding="0" cellspacing="0" class="sortable">';
	echo '<tr><th>Hashtag</th><th>Obtained at (DD-MM-YYYY)</th><th>Total Users</th><th>Total Promoters</th><th>Total Adopters</th><th>Total Tweets</th></tr>';
	foreach ($hashtags as $key => $hashtag) {
		echo '<tr>';
		echo '<td><a href="../app.php?query='. $hashtag["hashtag"] . '&date=' . date("d-m-Y", strtotime($hashtag["obtained_at"])) . '">#' . $hashtag["hashtag"] . '</a></td><td>' . date("d-m-Y", strtotime($hashtag["obtained_at"])) . '</td><td>' . $hashtag["n_users_total"] . '</td><td>' . $hashtag["n_users_promoter"] . '</td><td>' . $hashtag["n_users_adopter"] . '</td><td>' . $hashtag["tweet_count"] . '</td>';
		echo '</tr>';
	}
		echo '</table><br />';
	print "</body>
</html>";
}else{
	$hashtags = getHashtags($db);

	if($query[0] == "#")
		 $query = substr($query, 1);

	$dataType = "json";

	if(isset($_GET['dataType'])) {
		$dataType = $_GET['dataType'];
	}

	$found_hashtags = array();

	foreach ($hashtags as $key => $hashtag) {
		if (stristr($hashtag["hashtag"], $query) != false) {
			array_push($found_hashtags	, $hashtag);
		}
	}

	switch($dataType) {

		case "json":

			$json = '[';

			foreach($found_hashtags as $key => $hashtag) {
				$json .= '{"hashtag": "#' . $hashtag["hashtag"] . '"}';

				if ($hashtag !== end($found_hashtags)) {
					$json .= ',';
				}
			}

			$json .= ']';

			header('Content-Type: application/json');
			echo $json;

		break;

		case "xml":
	 	    $xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' . "\n";
			$xml .= '<data>';

			foreach($found_hashtags as $key => $hashtag) {
				$xml .= '<hashtag>' . $hashtag . '</hashtag>';
			}

			$xml .= '</data>';


			header('Content-Type: text/xml');
			echo $xml;
		break;

		default:
		break;
	}
}

?>
