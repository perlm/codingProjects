#!/usr/bin/perl

#51      39.8%   48      39.6%

while ($line = <STDIN>){
	chomp($line);
	@vars = split(/\s+/, $line);
	$r1=$vars[0];$fg2=substr($vars[1],0,-1);
	$r2=$vars[2];$fg1=substr($vars[3],0,-1);

	if ($fg2>$fg1){
		$dFG = $fg2-$fg1;
		$dR = $r2-$r1;
	}
	else{
		$dFG = $fg1-$fg2;
		$dR = $r1-$r2;
	}

	print "$dFG\t$dR\n";
}

exit;
