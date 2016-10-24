#!/usr/bin/perl -w

# plot 'switch.data' u 2:($3==0?$1:1/0) w p pt 7 ps 1, 'switch.data' u 2:($3==1?$1:1/0) w p pt 7 ps 1 lc 3, x lc rgb "dark-green" lw 3, x +0.05 lw 3 lc rgb "goldenrod"

#what fraction of these circumstances: worse shooter, same shooter, average better but not, much better

$file1 = 'data/freeThrows.data';
$file2 = 'data/techSwitches.data';

$outFile = "switch.data";
open OUT1, ">$outFile" or die "can't write to file.";
$outFile = "points.data";
open OUT2, ">$outFile" or die "can't write to file.";

%ftAve=();
open (CALC, $file1);
while ($line = <CALC>){
	chomp($line);
	@vars = split(/\s+/, $line);
	$ftAve{$vars[0]} = ($vars[1] + $vars[3] + $vars[5])/($vars[2] + $vars[4] + $vars[6]);
}
#foreach $k1 (sort keys %ftAve){print "$k1\t$ftAve{$k1}\n";}

@circumstance=();#0=worse shooter, 1=less than 5% better, 2=significantly better, 3 same guy
$count=0;
$simpleError=0;
$fancierError=0;
$count2=0;
$one=0;
open (CALC, $file2);
while ($line = <CALC>){
	#Jose-Calderon 1 Chris-Bosh 1 2 280220028
	chomp($line);
	@vars = split(/\s+/, $line);
	if ($vars[4]==1){
		$p1 = defined($ftAve{$vars[0]}) ? $ftAve{$vars[0]} : -1;
		$p2 = defined($ftAve{$vars[2]}) ? $ftAve{$vars[2]} : -1;
		$switch = $vars[0] eq $vars[2] ? 1:0;
		print OUT1 "$p1\t$p2\t$switch\n";

		$d = $p1-$p2;
		if ($switch){$circumstance[3]++;}
		elsif ($d<0){$circumstance[0]++;}
		elsif ($d<=0.05){$circumstance[1]++;}
		else{$circumstance[2]++;}
		$count+=1;

		if ($ftAve{$vars[0]}<0.7){print "$vars[0]\t$ftAve{$vars[0]}\t$vars[2]\t$ftAve{$vars[2]}\n";}

		$points = $vars[1] + $vars[3];
		$one=1;
	}
	elsif(($vars[4]==2) and ($one)){
		# -0.018887114322177 0.0231058621375531 0.0364739665650321
		$points += $vars[3];
		$one=0;
		$simpleExpectedPoints = $ftAve{$vars[0]} + 2*$ftAve{$vars[2]};
		if ($vars[0] eq $vars[2]){$fancierExpectedPoints = ($ftAve{$vars[0]}-0.018887114322177) + ($ftAve{$vars[0]}+0.0231058621375531) + ($ftAve{$vars[2]}+0.0364739665650321);}
		else{$fancierExpectedPoints = ($ftAve{$vars[0]}-0.018887114322177) + ($ftAve{$vars[2]}-0.018887114322177) + ($ftAve{$vars[2]}+0.0231058621375531);}

		print OUT2 "$ftAve{$vars[0]}\t$ftAve{$vars[2]}\t$points\t$simpleExpectedPoints\t$fancierExpectedPoints\n";

		$simpleError += ($points-$simpleExpectedPoints)**2;
		$fancierError += ($points-$fancierExpectedPoints)**2;
		$count2++;
	}
}

print "\nOutcomes:\n";
for ($c=0;$c<=3;$c++){
	$f = $circumstance[$c]/$count;
	print "$c\t$circumstance[$c]\t$count\t$f\n";
}
$simpleError = ($simpleError/$count2)**0.5;
$fancierError = ($fancierError/$count2)**0.5;
print "\nSimple Error: $simpleError\nFancier Error: $fancierError\n";


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
        #my $stde = $std/ (@$data**0.5);
        return $std;
}

sub bootstrap{
        my $success = $_[0];
        my $total = $_[1];
        my $frac = $success/$total;
        if (($frac==1) or ($frac==0)){return 0;}
        my @means=();
        my $sample=0;my $rand=0;my $mean=0;
        #for (my $i=0;$i<100000;$i++){
        for (my $i=0;$i<100;$i++){
                my @s=();
                for (my $t=0;$t<$total;$t++){
                        if (rand()<=$frac){$sample=1;}else{$sample=0;}
                        push (@s,$sample);
                }
                $mean=mean(\@s);
                push (@means,$mean);
        }

        my $std = std(\@means);
        return $std;
}



exit;
