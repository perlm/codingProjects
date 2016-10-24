#!/usr/bin/perl

#get 2d binned average

$min=50;
$max=150;
$binwidth=1;
%count=();
%winner=();

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
			$count{$b1}++;
			$count{$b2}++;

			$d1=abs($vars[0]-$vars[2]);
			$d2=abs($vars[1]-$vars[2]);
			
			if ($d1<$d2){$winner{$b1}+=1;}
			else{$winner{$b2}+=1;}
		}
	}
}

$bins=($max-$min)/$binwidth;
for($iii=0;$iii<=$bins;$iii++){
	$actual=$iii*$binwidth+$min;

	if ($count{$iii}){
		$w=$winner{$iii}/$count{$iii};
		print "$actual\t$w\n";
	}
}
exit;
