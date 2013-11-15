<?php
if (array_key_exists("temper",$_GET )) {
    $temper = $_GET["temper"];
    $file=fopen("temper.txt","w");
    fwrite($file, $temper);
    fclose($file);
    echo $temper;
} else {
    $temper = file_get_contents("temper.txt");
    echo $temper;
}

?>
