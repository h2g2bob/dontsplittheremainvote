<?php

$db = new SQLite3('../../../postcodes.sqlite3', SQLITE3_OPEN_READONLY);

$PC = preg_replace("/[^A-Z0-9]/", "", strtoupper($_POST['postcode']));

$stm = $db->prepare('SELECT slug FROM postcodes WHERE postcode = :postcode');
$stm->bindValue(':postcode', $PC, SQLITE3_TEXT);

$section = $_POST['section'];
if (!$section) {
	$section = 'constituency';
}

$res = $stm->execute();

$row = $res->fetchArray(SQLITE3_NUM);
if ($row) {
    header("location: /2019/${section}/${row[0]}.html");
} else {
    header("location: /2019/${section}/");
}

?>
