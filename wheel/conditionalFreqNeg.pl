#!/usr/bin/perl

#how does distribution change if you know that puzzle contains R,S,T,L,N,E...

%total=();
%data=();

$d{'A'}=8.167;
$d{'B'}=1.492;
$d{'C'}=2.782;
$d{'D'}=4.253;
$d{'E'}=12.702;
$d{'F'}=2.228;
$d{'G'}=2.015;
$d{'H'}=6.094;
$d{'I'}=6.966;
$d{'J'}=0.153;
$d{'K'}=0.772;
$d{'L'}=4.025;
$d{'M'}=2.406;
$d{'N'}=6.749;
$d{'O'}=7.507;
$d{'P'}=1.929;
$d{'Q'}=0.095;
$d{'R'}=5.987;
$d{'S'}=6.327;
$d{'T'}=9.056;
$d{'U'}=2.758;
$d{'V'}=0.978;
$d{'W'}=2.361;
$d{'X'}=0.150;
$d{'Y'}=1.974;
$d{'Z'}=0.074;


while ($line = <STDIN>){
	chomp($line);
	foreach (split //, $line) {
		if ($_ =~/[A-Z]/){
			$data{0}{$_}++;
			$total{0}++;
			if ($line !~ /R/){$data{1}{$_}++;$total{1}++;}
			if ($line !~ /S/){$data{2}{$_}++;$total{2}++;}
			if ($line !~ /T/){$data{3}{$_}++;$total{3}++;}
			if ($line !~ /L/){$data{4}{$_}++;$total{4}++;}
			if ($line !~ /N/){$data{5}{$_}++;$total{5}++;}
			if ($line !~ /E/){$data{6}{$_}++;$total{6}++;}
		}
	}
}

#print "# R-$total{1}, S-$total{2}, T-$total{3}, L-$total{4}, N-$total{5}, E-$total{6}, $total{0}\n";#total characters
foreach $k1 (sort { $data{0}{$b} <=> $data{0}{$a} } keys %{$data{0}}){
	$n = 100*$data{0}{$k1}/$total{0};
	$n1 = 100*$data{1}{$k1}/$total{1};
	$n2 = 100*$data{2}{$k1}/$total{2};
	$n3 = 100*$data{3}{$k1}/$total{3};
	$n4 = 100*$data{4}{$k1}/$total{4};
	$n5 = 100*$data{5}{$k1}/$total{5};
	$n6 = 100*$data{6}{$k1}/$total{6};
	print "$k1\t$n\t$d{$k1}\t$n1\t$n2\t$n3\t$n4\t$n5\t$n6\n";
}
exit;
