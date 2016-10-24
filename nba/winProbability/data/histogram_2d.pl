#!/usr/bin/perl

$min1=0;
$max1=50;
$min2=-50;
$max2=50;
$binwidth=1;

#time, score, winner...
#0 0 1
#1 0 1


while ($line = <STDIN>){
	chomp($line);
	@vars = split(/\s+/, $line);
	$t=$vars[0];$s=$vars[1];

	$b1 = int(($t-$min1)/$binwidth);
	$b2 = int(($s-$min2)/$binwidth);
	$bin{$b1}{$b2}++;
	if ($vars[2]==1){$prob{$b1}{$b2} +=1;}elsif($vars[2]==-1){$prob{$b1}{$b2} += 0;}
}

$bins1=($max1-$min1)/$binwidth;
$bins2=($max2-$min2)/$binwidth;
for($iii=0;$iii<=$bins1;$iii++){for($jjj=0;$jjj<=$bins2;$jjj++){
	$actual1=$iii*$binwidth+$min1;$actual2=$jjj*$binwidth+$min2;

	$n=$bin{$iii}{$jjj};
	if(!$n){$n=0;$p=-1;}
	else{$p=$prob{$iii}{$jjj}/$bin{$iii}{$jjj};}
	print "$actual1\t$actual2\t$n\t$p\n";
}}
exit;
