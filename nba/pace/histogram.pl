#!/usr/bin/perl

$min=85;
$max=105;
$binwidth=1;
%bin=();

@files =  <data/seasonAve_20*.data>;

foreach $file (@files){
	@vars=();
        open (CALC, $file);
        while ($line = <CALC>){
		chomp($line);
		@vars = split(/\s+/, $line);
		$b = int(($vars[1]-$min)/$binwidth);
		$bin{$b}++;
	}
}

$bins=($max-$min)/$binwidth;
for($iii=0;$iii<=$bins;$iii++){
	$actual=$iii*$binwidth+$min;
	$b1=$bin{$iii};
	print "$actual\t$b1\n";
}
exit;
