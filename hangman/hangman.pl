#!/usr/bin/perl

my $lives=7;
my $word = wordPick();
my %guesses=();
my $guessed="";
my @letters = ('a'..'z');
my @lettersFreq = ('e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z');
my $done=0;

while ($lives){
	#guess
	my $g="";
	for ($i=0;!$g;$i++){
		#$g = $letters[(int(rand(scalar(@letters))))];	#random
		$g = $lettersFreq[($i)];			#most frequent
		if ($guesses{$g}){$g="";}
		else{
			$guesses{$g}=1;
			$guessed .= "\$g";
		}
	}
	print "Guess is $g\n";
	if ($word !~ m/$g/){$lives--;}

	#display and decide if win/lose
	$wordDisplay = $word;
	foreach $l (@letters){if (!$guesses{$l}){$wordDisplay =~ s/$l/_/g;}}
	print "$word $wordDisplay ";
	if (!$lives){print "LOSER!\n";}
	else{
		$done=1;
		foreach $l (@letters){
			if (!$guesses{$l}){
				if ($word =~ m/$l/){$done=0;}
			}
		}
		if ($done){print "Winner!\n";}
		else{print "$lives lives left\n";}
	}
	if ($done){last;}
}


sub wordPick{
	my $dictionary = "/usr/share/dict/words";
	my $word=0;
	until ($word){
		$pick = int(rand(99171));
		$l=0;
		open (DICT, "<", $dictionary) or die "cannot open $dictionary\n";
		while ($line = <DICT>){
			chomp($line);
			if ($l==$pick){$word = $line;}
			$l++;
		}
		if ($word =~ m/[A-Z]/){$word="";}
	}
	return $word;
}

exit;
