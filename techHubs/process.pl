#!/usr/bin/perl



%cites=();
open (CALC, '../UScities.data');
while ($line = <CALC>){
	chomp($line);
	@vars = split(/\t/, $line);
	if (!$cities{$vars[0]}){
		$cities{$vars[0]} = $vars[1] . " " . $vars[2]; 
	}
}

open (CALC, 'techhub.data');
while ($line = <CALC>){
	chomp($line);
	@vars = split(/\s+/, $line);
	$city=$vars[0];
	$city =~ tr/_/ /;
	if ($cities{$city}){print "$vars[0] $vars[1] $cities{$city}\n";}
	else{print "$city not found!\n";}
}

exit;
