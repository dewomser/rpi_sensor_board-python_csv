<?php
if (array_key_exists("x",$_GET ) && array_key_exists("y",$_GET )) {
    $x = $_GET["x"];
    $y = $_GET["y"];
    $file=fopen("gsensor.txt","w");
    fprintf($file, "%d %d", $x, $y);
    fclose($file);
    //echo $x;
} else {
    $file=fopen("gsensor.txt","r");
    fscanf($file, "%d %d", $x, $y);
    fclose($file);
    //echo $x;
    //echo $y;
    printf("%d %d",$x, $y);
}

?>