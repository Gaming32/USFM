#!/usr/bin/php
<?php

$launcher = 'python3';
$program = 'findsfm.py';

$malbookdict = array(
    'Gen'=> 'ഉല്‍പത്തി',
    'Exo'=> 'പുറപ്പാടു്',
    'Lev'=> 'ലേവ്യപുസ്തകം',
    'Psa'=> 'സബൂർ',
    'Isa'=> 'യെശയ്യാവു',
    'Mat'=> 'മത്തായി',
    'Mar'=> 'മർക്കൊസ്',
    'Luk'=> 'ലൂക്കാ',
    'Joh'=> 'യോഹന്നാൻ',
    'Act'=> 'പ്രവൃത്തികൾ',
    'Rom'=> 'റോമർ'
);

if ($argc <2) {
    echo "Syntax: $argv[0] <scripture-references>\n\n";
    echo "Scripture references should be comma delimited\n";
    exit(1);
}
if (isset($argv[2])) $fileout = ">>" . array_pop($argv);
array_shift($argv);

$args = implode(' ',$argv);

$output = '';

foreach (preg_split("/\s*[,;]\s*/",$args) as $ix => $ref) {
    $output .= "$launcher $program --no-v-markings $ref";
    if ($ix == 0) $output .= " \"$args\"";
    $output .= " $fileout\n";
}

echo $output;
#echo shell_exec($output);