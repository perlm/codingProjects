#!/usr/bin/perl

$min=0;
$max=100;
$binwidth=1;

@bin=();
@count=();
while ($line = <STDIN>){
	chomp($line);
	@vars = split(/\s+/, $line);
	#$4, $5
        $b = int($vars[3]/$binwidth);
       	$bin[$b]+=$vars[5]-1; 
       	$count[$b]++;
}

$bins=($max-$min)/$binwidth;
for($iii=0;$iii<=$bins;$iii++){
	$actual=$iii*$binwidth+$min;
	if ($count[$iii]){
		$prob = 1- ($bin[$iii]/$count[$iii]);
		print "$actual\t$prob\n";
	}
}
exit;
