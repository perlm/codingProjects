#!/usr/bin/perl -w

# data/showgame.php?game_id=1644
@files =   <data/show*>;

%clue=();
$shows=0;
$totalClues=0;

foreach $file (@files){
        $file =~ m/id=([0-9]*)/g;
        #$f=$1;

	#@vars=();
	$show=0;$year=0;
	open (CALC, $file);
	while ($line = <CALC>){
		chomp($line);
		#@vars = split(/\s+/, $line);
		#Show #4596, aired 2004-09-06
		if ($line =~ m/[Ss]how #([0-9]*).* aired ([12][0-9][0-9][0-9])-/g){
			$show = $1;
			$year = $2*1.0;
			$decade = int($year/10);
			$shows+=1;
		}
		#regular clues
		elsif ($line =~ m/correct_response&quot;&gt;the \&lt;i\&gt;([A-Za-z][\w\W\s]*?)\&lt;\/i/g){
			$clue{$1}{$decade}+=1;
			$totalClues+=1;
		}
		elsif ($line =~ m/correct_response&quot;\&gt;(\(?[A-Za-z][\w\W\s]*?)\&lt;/g){
			$clue{$1}{$decade}+=1;
			$totalClues+=1;
		}
		elsif ($line =~ m/correct_response&quot;\&gt;\&lt;i\&gt;(\(?[A-Za-z][\w\W\s]*?)\&lt;/g){
			$clue{$1}{$decade}+=1;
			$totalClues+=1;
		}
		elsif ($line =~ m/correct_response&quot;\&gt;\&quot;(\(?[A-Za-z][\w\W\s]*?)\&quot;\&lt;/g){
			$clue{$1}{$decade}+=1;
			$totalClues+=1;
		}
		#final clues
		elsif ($line =~ m/correct_response\\&quot;\&gt;the \&lt;i\&gt;(\(?[A-Za-z][\w\W\s]*?)\&lt;/g){
			$clue{$1}{$decade}+=1;
			$totalClues+=1;
		}
		elsif ($line =~ m/correct_response\\&quot;&gt;(\(?[A-Za-z][\w\W\s]*?)&lt;/g){
			$clue{$1}{$decade}+=1;
			$totalClues+=1;
		}
		elsif ($line =~ m/correct_response\\&quot;&gt;&lt;i&gt;(\(?[A-Za-z][\w\W\s]*?)&lt;/g){
			$clue{$1}{$decade}+=1;
			$totalClues+=1;
		}
	}
}
#print "$shows $totalClues\n";

#mostFrequent(%clue);
#stateFreq(%clue);
#planets(%clue);
#henry(%clue);
#presidents(%clue);
decadeSwing(%clue);



sub decadeSwing{
	my (%clue) = @_;
	#print out most frequent:
	$name1 = "decadeSwing.data";
	open OUT1, ">$name1" or die "can't write to file.";
	%diff=();
	my $d=0;
	my $total1=0;my $total2=0;

	$past=199;	#change to 198 for 80s.
	foreach my $name (%clue){
		if (!defined($clue{$name}{201})){$clue{$name}{201}=0;}
		if (!defined($clue{$name}{$past})){$clue{$name}{$past}=0;}
		$total1 += $clue{$name}{$past};
		$total2 += $clue{$name}{201};
		$d = $clue{$name}{201} - $clue{$name}{$past};
		$diff{$name}=$d;
	}
	foreach my $name (sort { $diff{$b} <=> $diff{$a} } keys %diff){print OUT1 "$name\t$diff{$name}\n";}
	print "Total 2010s = $total2, Total 1980s = $total1\n";
}
sub mostFrequent{
	my (%clue) = @_;
	#print out most frequent:
	$name1 = "mostFrequent.data";
	open OUT1, ">$name1" or die "can't write to file.";
	foreach my $name (sort { $clue{$b} <=> $clue{$a} } keys %clue){print OUT1 "$name\t$clue{$name}\n";}
}
sub henry{
	my (%clue) = @_;
	#print out frequency only for wives of Henry VIII
	$name1 = "henry.data";
	open OUT1, ">$name1" or die "can't write to file.";
	my @wifeNames = ('Catherine of Aragon', 'Anne Boleyn', 'Jane Seymour', 'Anne of Cleves', 'Catherine Howard', 'Catherine Parr');
	my @wives=();
	#the names are formatted somewhat weird so do it this way:
	foreach my $c (%clue){
		if ((index($c, 'atherine' ) != -1) and (index($c, 'Aragon' ) != -1)){$wives[0]+=$clue{$c};}
		if ((index($c, 'Anne' ) != -1) and (index($c, 'Boleyn' ) != -1)){$wives[1]+=$clue{$c};}
		if ((index($c, 'Jane' ) != -1) and (index($c, 'Seymour' ) != -1)){$wives[2]+=$clue{$c};}
		if ((index($c, 'Anne' ) != -1) and (index($c, 'Cleves' ) != -1)){$wives[3]+=$clue{$c};}
		if ((index($c, 'atherine' ) != -1) and (index($c, 'Howard' ) != -1)){$wives[4]+=$clue{$c};}
		if ((index($c, 'atherine' ) != -1) and (index($c, 'Parr' ) != -1)){$wives[5]+=$clue{$c};}
	}
	for ($w=0;$w<scalar(@wifeNames);$w++){print OUT1 "$wifeNames[$w] $wives[$w]\n";}
}
sub presidents{
	my (%clue) = @_;
	#print out frequency only for presidents
	$name1 = "presidents.data";
	open OUT1, ">$name1" or die "can't write to file.";
	@pres=();
	push(@pres,[qw(George Washington)]);
	push(@pres,[qw(John Adams)]);
	push(@pres,[qw(Thomas Jefferson)]);
        push(@pres,[qw(James Madison)]);
        push(@pres,[qw(James Monroe)]);
        push(@pres,[qw(John Quincy Adams)]);
        push(@pres,[qw(Andrew Jackson)]);
        push(@pres,[qw(Martin Van Buren)]);
        push(@pres,[qw(William Harrison)]);
        push(@pres,[qw(John Tyler)]);
        push(@pres,[qw(James Polk)]);
        push(@pres,[qw(Zachary Taylor)]);
        push(@pres,[qw(Millard Fillmore)]);
        push(@pres,[qw(Franklin Pierce)]);
        push(@pres,[qw(James Buchanan)]);
        push(@pres,[qw(Abraham Lincoln)]);
        push(@pres,[qw(Andrew Johnson)]);
        push(@pres,[qw(Ulysses Grant)]);
        push(@pres,[qw(Rutherford Hayes)]);
        push(@pres,[qw(James Garfield)]);
        push(@pres,[qw(Chester Arthur)]);
        push(@pres,[qw(Grover Cleveland)]);
        push(@pres,[qw(Benjamin Harrison)]);
        push(@pres,[qw(Grover Cleveland)]);
        push(@pres,[qw(William McKinley)]);
        push(@pres,[qw(Theodore Roosevelt)]);
        push(@pres,[qw(William Taft)]);
        push(@pres,[qw(Woodrow Wilson)]);
        push(@pres,[qw(Warren Harding)]);
        push(@pres,[qw(Calvin Coolidge)]);
        push(@pres,[qw(Herbert Hoover)]);
        push(@pres,[qw(Franklin Roosevelt)]);
        push(@pres,[qw(Harry Truman)]);
        push(@pres,[qw(Dwight Eisenhower)]);
        push(@pres,[qw(John Kennedy)]);
        push(@pres,[qw(Lyndon Johnson)]);
        push(@pres,[qw(Richard Nixon)]);
        push(@pres,[qw(Gerald Ford)]);
        push(@pres,[qw(Jimmy Carter)]);
        push(@pres,[qw(Ronald Reagan)]);
        push(@pres,[qw(George H. W. Bush)]);
        push(@pres,[qw(Bill Clinton)]);
        push(@pres,[qw(George W. Bush)]);
        push(@pres,[qw(Barack Obama)]);
	@presidents=();
	#the names are formatted somewhat weird so do it this way:
	foreach my $c (%clue){
		for (my $p=0;$p<scalar(@pres);$p++){
			if ( ($p!=23) and ($p!=1) and ($p!=5) and ($p!=40) and ($p!=42)){if ((index($c,$pres[$p][0])!=-1) and (index($c,$pres[$p][1])!=-1)){$presidents[$p]+=$clue{$c};}}
			elsif ($p==1){
				if ((index($c,$pres[$p][0])!=-1) and (index($c,$pres[$p][1])!=-1)){
					if (index($c,'Quincy')!=-1){$presidents[5]+=$clue{$c};}
					else{$presidents[1]+=$clue{$c};}
				}
			}
			elsif ($p==40){
				if ((index($c,'George')!=-1) and (index($c,'Bush')!=-1)){
					#if there's an H it's definitely 40. If there's no H and there is a W, its 42. If there's no h or w call it 40.
					if (index($c,'H')!=-1){$presidents[40]+=$clue{$c};}
					elsif (index($c,'W')!=-1){$presidents[42]+=$clue{$c};}
					else{$presidents[40]+=$clue{$c};}
				}
			}
			elsif (($p==42) or ($p==1)){next;} 	#shouldn't loop through 40 and 42 separately
		}
	}
	$presidents[23]=$presidents[21];
	for ($w=0;$w<scalar(@pres);$w++){print OUT1 "@{@pres[$w]} $presidents[$w]\n";}
}
sub planets{
	my (%clue) = @_;
	#print out frequency only for planets
	$name1 = "planets.data";
	open OUT1, ">$name1" or die "can't write to file.";
	my @planets = ('Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto');
	foreach my $name (@planets){print OUT1 "$name\t$clue{$name}\n";}
}
sub stateFreq{
	my (%clue) = @_;
	#print out frequency only for states
	$name1 = "states.data";
	open OUT1, ">$name1" or die "can't write to file.";
	#my @states= ('Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming');
	my $string = <<'END';
Massachusetts
Minnesota
Montana
North Dakota
Idaho
Washington
Arizona
California
Colorado
Nevada
New Mexico
Oregon
Utah
Wyoming
Arkansas
Iowa
Kansas
Missouri
Nebraska
Oklahoma
South Dakota
Louisiana
Texas
Connecticut
New Hampshire
Rhode Island
Vermont
Alabama
Florida
Georgia
Mississippi
South Carolina
Illinois
Indiana
Kentucky
North Carolina
Ohio
Tennessee
Virginia
Wisconsin
West Virginia
Delaware
Maryland
New Jersey
New York
Pennsylvania
Maine
Michigan
Hawaii
Alaska
END
	my @states = split /\n/, $string;
	foreach my $name (@states){
		print OUT1 "$name\t$clue{$name}\n";
		print "$clue{$name} ";
	}
	
}

exit;
