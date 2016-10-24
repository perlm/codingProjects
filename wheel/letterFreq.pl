#!/usr/bin/perl

$total=0;
%data=();

$d{'A'}=8.167;
$d{'B'}=1.492;
$d{'C'}=2.782;
$d{'D'}=4.253;
$d{'E'}=12.702;
$d{'F'}=2.228;
$d{'G'}=2.015;
$d{'H'}=6.094;
$d{'I'}=6.966;
$d{'J'}=0.153;
$d{'K'}=0.772;
$d{'L'}=4.025;
$d{'M'}=2.406;
$d{'N'}=6.749;
$d{'O'}=7.507;
$d{'P'}=1.929;
$d{'Q'}=0.095;
$d{'R'}=5.987;
$d{'S'}=6.327;
$d{'T'}=9.056;
$d{'U'}=2.758;
$d{'V'}=0.978;
$d{'W'}=2.361;
$d{'X'}=0.150;
$d{'Y'}=1.974;
$d{'Z'}=0.074;


while ($line = <STDIN>){
	chomp($line);
	foreach (split //, $line) {
		if ($_ =~/[A-Z]/){
			$data{$_}++;
			$total++;
		}
	}
}
#foreach $k1 (sort keys %data){
foreach $k1 (sort { $data{$b} <=> $data{$a} } keys %data){
	$n = 100*$data{$k1}/$total;
	print "$k1\t$n\t$d{$k1}\n";
}
exit;
