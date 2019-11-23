<?php

$db = new SQLite3('postcodes.sqlite3', SQLITE3_OPEN_READONLY);

$PC = preg_replace("/[^A-Z0-9]/", "", strtoupper($_POST['postcode']));

$stm = $db->prepare('SELECT slug FROM postcodes WHERE postcode = :postcode');
$stm->bindValue(':postcode', $PC, SQLITE3_TEXT);

$res = $stm->execute();

$row = $res->fetchArray(SQLITE3_NUM);
if ($row) {
    header("location: /minimal/${row[0]}.html");
} else {
    header("location: /minimal/");
}

?>
