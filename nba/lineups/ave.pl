#!/usr/bin/perl


$sep=2.0;
%data=();

@label = qw(OffensiveEfficiency DefensiveEfficiency OpposingEFG OpposingTO OpposingORB OpposingSecondChancePts OpposingFastBreakPts OpposingPtsInPaint);

$file = 'data/lineupHeightStats.data';
open (CALC, $file);
while ($line = <CALC>){
	chomp($line);
	@vars = split(/\s+/, $line);
	for ($n=2;$n<=9;$n++){
		$i = $n-2;
		if ($vars[1]<=$sep){push (@{$data{$i}{0}}, $vars[$n]);}
		else{push (@{$data{$i}{1}}, $vars[$n]);}
	}
}


for ($i=0;$i<=7;$i++){
	$m0 = mean(\@{$data{$i}{0}});
	$m1 = mean(\@{$data{$i}{1}});
	$s0 = std(\@{$data{$i}{0}});
	$s1 = std(\@{$data{$i}{1}});
	print "$label[$i]\t$m0\t$s0\t$m1\t$s1\n";
}

sub mean{
        my($data) = @_;
        if (not @$data) {return 10000;}
        my $total = 0;
        foreach (@$data) {$total += $_;}
        my $average = $total / @$data;
        return $average;
}
sub std{
        my($data) = @_;
        if(@$data <= 1){return 0;}
        my $average = &mean($data);
        my $sqtotal = 0;
        foreach(@$data) {$sqtotal += ($average-$_) ** 2;}
        my $std = ($sqtotal / (@$data-1)) ** 0.5;
        my $stde = $std/ (@$data**0.5);
        return $stde;
}

exit;
