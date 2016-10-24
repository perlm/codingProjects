#!/usr/bin/perl

$min=0;
$max=100;
$binwidth=3;

while ($line = <STDIN>){
	chomp($line);
	@vars = split(/\s+/, $line);
	$fg = substr($vars[0],0,-1);
	$fg3 = substr($vars[1],0,-1);

	$b = int(($fg-$min)/$binwidth);
	$bin1{$b}++;
	$b = int(($fg3-$min)/$binwidth);
	$bin2{$b}++;
}

$bins=($max-$min)/$binwidth;
for($iii=0;$iii<=$bins;$iii++){
	$actual=$iii*$binwidth+$min;
	$b1=$bin1{$iii}/82;
	$b2=$bin2{$iii}/82;
	print "$actual\t$b1\t$b2\n";
}
exit;
