#!/usr/bin/perl

#get 2d binned average

$min=50;
$max=150;
$binwidth=1;
%bin=();
%count=();

@files =  <data/games*.data>;

foreach $file (@files){
	@vars=();
        open (CALC, $file);
        while ($line = <CALC>){
		chomp($line);
		@vars = split(/\s+/, $line);
		$b1 = int(($vars[0]-$min)/$binwidth);
		$b2 = int(($vars[1]-$min)/$binwidth);
		if (($vars[0]>$min) and ($vars[0]<$max) and ($vars[1]>$min) and ($vars[1]<$max)){
			$bin{$b1}{$b2}+=$vars[2];
			$count{$b1}{$b2}++;
		}
	}
}

$bins=($max-$min)/$binwidth;
for($iii=0;$iii<=$bins;$iii++){
	for($jjj=0;$jjj<=$bins;$jjj++){
	$actual=$iii*$binwidth+$min;
	$actual2=$jjj*$binwidth+$min;

	if ($count{$iii}{$jjj}){
		$a=$bin{$iii}{$jjj}/$count{$iii}{$jjj};
		print "$actual\t$actual2\t$a\n";
	}
}}
exit;
