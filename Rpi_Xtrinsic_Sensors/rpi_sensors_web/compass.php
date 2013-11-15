<?php
if (array_key_exists("heading",$_GET )) {
    $heading = $_GET["heading"];
    $file=fopen("compass.txt","w");
    fwrite($file, $heading);
    fclose($file);
    echo $heading;
} else {
    $heading = file_get_contents("compass.txt");
    echo $heading;
}

?>