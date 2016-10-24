#!/usr/bin/perl

$min=0;
$max=100;
$binwidth=1;

while ($line = <STDIN>){
	chomp($line);
	@vars = split(/\s+/, $line);
	$r=$vars[0];$fg=substr($vars[1],0,-1);
	$b1 = int(($r-$min)/$binwidth);
	$b2 = int(($fg-$min)/$binwidth);
	$bin{$b1}{$b2}++;
	$r=$vars[2];$fg=substr($vars[3],0,-1);
	$b1 = int(($r-$min)/$binwidth);
	$b2 = int(($fg-$min)/$binwidth);
	$bin{$b1}{$b2}++;
}

$bins=($max-$min)/$binwidth;
for($iii=0;$iii<=$bins;$iii++){for($jjj=0;$jjj<=$bins;$jjj++){
	$actual1=$iii*$binwidth+$min;$actual2=$jjj*$binwidth+$min;

	$b1=$bin{$iii}{$jjj};if(!$b1){$b1=0;}
	print "$actual1\t$actual2\t$b1\n";
	#$b2=$bin2{$iii}{$jjj};if(!$b2){$b2=0;}
	#print "$actual1\t$actual2\t\t$b1\t$b2\n";
}}
exit;
