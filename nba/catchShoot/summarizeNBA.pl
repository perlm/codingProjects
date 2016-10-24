#!/usr/bin/perl -w

#./summarizeNBA.pl catchAndShootForwards.data team_4ft.data team_6ft.data > summary_forwards.data

##2014-15 REGULAR SEASON PLAYER GENERAL RANGE (CATCH AND SHOOT)
##Player	Team	Age	GP	G	Freq	FGM	FGA	FG%	eFG%	2FG Freq	2FGM	2FGA	2FG%	3FG Freq	3PM	3PA	3P%
#Bosh, Chris	MIA	31	44	44	40.2%	3.2	6.8	46.5	56.7	19.6%	1.8	3.3	53.4	20.6%	1.4	3.5	39.9
#Bargnani, Andrea	NYK	29	29	27	52.2%	3.0	6.5	46.3	50.0	41.4%	2.5	5.1	49.0	10.8%	0.5	1.3	35.9

%dataAll=();
%data3pt=();

$abr{'Atlanta Hawks'}='ATL';$abr{'Los Angeles Clippers'}='LAC';$abr{'Portland Trail Blazers'}='POR';$abr{'Golden State Warriors'}='GSW';$abr{'Orlando Magic'}='ORL';$abr{'San Antonio Spurs'}='SAS';$abr{'Dallas Mavericks'}='DAL';$abr{'Houston Rockets'}='HOU';$abr{'Milwaukee Bucks'}='MIL';$abr{'Philadelphia 76ers'}='PHI';$abr{'Washington Wizards'}='WAS';$abr{'Boston Celtics'}='BOS';$abr{'Phoenix Suns'}='PHX';$abr{'Oklahoma City Thunder'}='OKC';$abr{'Utah Jazz'}='UTA';$abr{'Indiana Pacers'}='IND';$abr{'New Orleans Pelicans'}='NOP';$abr{'Cleveland Cavaliers'}='CLE';$abr{'Memphis Grizzlies'}='MEM';$abr{'Chicago Bulls'}='CHI';$abr{'New York Knicks'}='NYK';$abr{'Brooklyn Nets'}='BKN';$abr{'Detroit Pistons'}='DET';$abr{'Sacramento Kings'}='SAC';$abr{'Charlotte Hornets'}='CHA';$abr{'Denver Nuggets'}='DEN';$abr{'Minnesota Timberwolves'}='MIN';$abr{'Miami Heat'}='MIA';$abr{'Los Angeles Lakers'}='LAL';$abr{'Toronto Raptors'}='TOR';


my ($file1, $file2, $file3) = @ARGV;

open my $fh1, '<', $file1;
while ($line = <$fh1>){
	chomp($line);
	@vars=();
	@vars = split(/\t/, $line);
	$check = substr($vars[0],0,1);
	if ($check ne '#'){
		$entries = scalar(@vars);if ($entries ne "18"){print "Wrong number of columns 18 ne $entries\n";}
		$team = $vars[1];
		$allAttempts = $vars[7];
		if ($allAttempts>0){
			$allPercent = $vars[9];#8 is fg%, 9 is efg%
			$dataAll{$team}{0}+=$allAttempts*$allPercent*$vars[3];
			$dataAll{$team}{1}+=$allAttempts*$vars[3];
		}
		$threeAttempts = $vars[16];
		if ($threeAttempts>0){
			$threePercent = $vars[17];
			$data3pt{$team}{0}+=$threeAttempts*$threePercent*$vars[3];
			$data3pt{$team}{1}+=$threeAttempts*$vars[3];
		}
	}
}

##Team   GP      G       Freq    FGM     FGA     FG%     eFG%    2FG Freq        2FGM    2FGA    2FG%    3FG Freq        3PM     3PA     3P%
#Atlanta Hawks   82      82      24.7%   9.2     20.1    46.1    58.7    8.9%    4.2     7.2     57.8    15.8%   5.1     12.8    39.4
#Los Angeles Clippers    82      82      23.1%   8.8     19.2    45.8    57.0    10.3%   4.5     8.5     52.8    12.8%   4.3     10.7    40.3

#team 4 ft
open my $fh2, '<', $file2;
while ($line = <$fh2>){
	chomp($line);
	@vars=();
	@vars = split(/\t/, $line);
	$check = substr($vars[0],0,1);
	$team="";
	if ($check ne '#'){
		#$entries = scalar(@vars);print "$entries\n";
		$team = $abr{$vars[0]};
		$openAttempts{$team} = $vars[5];
		$openThrees{$team} = $vars[14];
	}
}

#team 6 ft
open my $fh3, '<', $file3;
while ($line = <$fh3>){
	chomp($line);
	@vars=();
	@vars = split(/\t/, $line);
	$check = substr($vars[0],0,1);
	$team="";
	if ($check ne '#'){
		#$entries = scalar(@vars);print "$entries\n";
		$team = $abr{$vars[0]};
		$openAttempts{$team} += $vars[5];
		$openThrees{$team} += $vars[14];
	}
}
print "Team\tFG%\tFGatt\t3%\t3Att\tTeamOpen\tTeamOpen3\n";
foreach $team (sort keys %dataAll){
	$allPercent = $dataAll{$team}{0}/$dataAll{$team}{1};	
	if ($data3pt{$team}{1}){$threePercent = $data3pt{$team}{0}/$data3pt{$team}{1};}else{$threePercent=0;$data3pt{$team}{1}=0;}
	print "$team\t$allPercent\t$dataAll{$team}{1}\t$threePercent\t$data3pt{$team}{1}\t$openAttempts{trim($team)}\t$openThrees{trim($team)}\n";
}

sub trim {
    (my $s = $_[0]) =~ s/^\s+|\s+$//g;
    return $s;        
}

exit;
