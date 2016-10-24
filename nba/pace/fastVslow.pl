#!/usr/bin/perl

#get frequency of outcomes when fast plays slow.

$fast=97;
$slow=91.5;
$veryFast=100;

$min=85;
$max=105;
$binwidth=1;
%bin=();$count1=0;
%bin2=();$count2=0;
%bin3=();$count3=0;
%bin4=();$count4=0;

@files =  <data/games*.data>;

foreach $file (@files){
	@vars=();
        open (CALC, $file);
        while ($line = <CALC>){
		chomp($line);
		@vars = split(/\s+/, $line);
		$b = int(($vars[2]-$min)/$binwidth);
		if (($vars[0]>$min) and ($vars[0]<$max) and ($vars[1]>$min) and ($vars[1]<$max)){
			if ((($vars[0]>$fast) and ($vars[1]<$slow)) or (($vars[1]>$fast) and ($vars[0]<$slow))){$bin{$b}++;$count1++;}
			elsif (($vars[0]<$slow) and ($vars[0]<$slow)){$bin2{$b}++;$count2++;}
			elsif (($vars[0]>$fast) and ($vars[1]>$fast)){$bin3{$b}++;$count3++;}
			if ((($vars[0]>$veryFast) and ($vars[1]<$slow)) or (($vars[1]>$veryFast) and ($vars[0]<$slow))){$bin4{$b}++;$count4++;}
		}
	}
}

$bins=($max-$min)/$binwidth;
for($iii=0;$iii<=$bins;$iii++){
	$actual=$iii*$binwidth+$min;
	if (not $bin{$iii}){$bin{$iii}=0;}else{$bin{$iii}=$bin{$iii}/$count1;}
	if (not $bin2{$iii}){$bin2{$iii}=0;}else{$bin2{$iii}=$bin2{$iii}/$count2;}
	if (not $bin3{$iii}){$bin3{$iii}=0;}else{$bin3{$iii}=$bin3{$iii}/$count3;}
	if (not $bin4{$iii}){$bin4{$iii}=0;}else{$bin4{$iii}=$bin4{$iii}/$count4;}
	print "$actual\t$bin{$iii}\t$bin2{$iii}\t$bin3{$iii}\t$bin4{$iii}\n";
}
print "Total number of games = $count1 $count2 $count3 $count4\n";
exit;
