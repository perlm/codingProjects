#!/usr/bin/perl

$min=0;
$binwidth1=1;
$binwidth2=5000;

@bin=();
@count=();
while ($line = <STDIN>){
	chomp($line);
	@vars = split(/\s+/, $line);
	#$4, $5
        $b1 = int($vars[3]/$binwidth1);
        $b2 = int($vars[4]/$binwidth2);
       	$bin[$b1][$b2]+=$vars[5]-1; 
       	$count[$b1][$b2]++;
}

$bins1=(100-$min)/$binwidth1;
$bins2=(100000-$min)/$binwidth2;
for($iii=0;$iii<=$bins1;$iii++){
	for($jjj=0;$jjj<=$bins2;$jjj++){

	$actual1=$iii*$binwidth1+$min;
	$actual2=$jjj*$binwidth2+$min;

	if ($count[$iii][$jjj]){
		$prob = 1- ($bin[$iii][$jjj]/$count[$iii][$jjj]);
		print "$actual1\t$actual2\t$prob\n";
	}
}
}
exit;
