#!/usr/bin/perl -w

#./summarizeNBA.pl  technicals.raw >summary.data

#$abr{'Atlanta Hawks'}='ATL';$abr{'Los Angeles Clippers'}='LAC';$abr{'Portland Trail Blazers'}='POR';$abr{'Golden State Warriors'}='GSW';$abr{'Orlando Magic'}='ORL';$abr{'San Antonio Spurs'}='SAS';$abr{'Dallas Mavericks'}='DAL';$abr{'Houston Rockets'}='HOU';$abr{'Milwaukee Bucks'}='MIL';$abr{'Philadelphia 76ers'}='PHI';$abr{'Washington Wizards'}='WAS';$abr{'Boston Celtics'}='BOS';$abr{'Phoenix Suns'}='PHX';$abr{'Oklahoma City Thunder'}='OKC';$abr{'Utah Jazz'}='UTA';$abr{'Indiana Pacers'}='IND';$abr{'New Orleans Pelicans'}='NOP';$abr{'Cleveland Cavaliers'}='CLE';$abr{'Memphis Grizzlies'}='MEM';$abr{'Chicago Bulls'}='CHI';$abr{'New York Knicks'}='NYK';$abr{'Brooklyn Nets'}='BKN';$abr{'Detroit Pistons'}='DET';$abr{'Sacramento Kings'}='SAC';$abr{'Charlotte Hornets'}='CHA';$abr{'Denver Nuggets'}='DEN';$abr{'Minnesota Timberwolves'}='MIN';$abr{'Miami Heat'}='MIA';$abr{'Los Angeles Lakers'}='LAL';$abr{'Toronto Raptors'}='TOR';


#place of birth: http://www.hoopsrumors.com/2015/01/foreign-salaries-country.html
@int = ('Manu Ginobili', 'Luis Scola', 'Pablo Prigioni', 'Tony Parker', 'Mirza Teletovic', 'Bojan Bogdanovic', 'Jusuf Nurkic', 'Ognjen Kuzmic', 'Nene', 'Anderson Varejao', 'Tiago Splitter', 'Lucas Nogueira', 'Bruno Caboclo', 'Leandro Barbosa', 'Joel Embiid', 'Luc Mbah a Moute', 'Damjan Rudez', 'Bismack Biyombo', 'Al Horford', 'Nicolas Batum', 'Boris Diaw', 'Ian Mahinmi', 'Evan Fournier', 'Rudy Gobert', 'Alexis Ajinca', 'Damien Inglis', 'Kevin Seraphin', 'Zaza Pachulia', 'Dirk Nowitzki', 'Carlos Boozer', 'Dennis Schröder', 'Kostas Papanikolaou', 'Giannis Antetokounmpo', 'Omri Casspi', 'Andrea Bargnani', 'Danilo Gallinari', 'Marco Belinelli', 'Reggie Jackson', 'Luigi Datome', 'Jerome Jordan', 'Jonas Valanciunas', 'Donatas Motiejunas', 'Pero Antic', 'Jorge Gutierrez', 'Nikola Pekovic', 'Nikola Mirotic', 'Festus Ezeli', 'Marcin Gortat', 'J.J. Barea', 'Serge Ibaka', 'Timofey Mozgov', 'Andrei Kirilenko', 'Alexey Shved', 'Sergey Karasev', 'Gorgui Dieng', 'Goran Dragic', 'Beno Udrih', 'Zoran Dragic', 'Marc Gasol', 'Pau Gasol', 'Jose Calderon', 'Ricky Rubio', 'Victor Claver', 'Luol Deng', 'Jonas Jerebko', 'Jeff Taylor', 'Enes Kanter', 'Thabo Sefolosha', 'Nikola Vucevic', 'Clint Capela', 'Omer Asik', 'Ersan Ilyasova', 'Furkan Aldemir', 'Hedo Turkoglu', 'Alex Len', 'Greivis Vasquez', 'Tim Duncan');

#canada, australia, and England, new zealand
@intEnglish = ('Andrew Bogut', 'Kyrie Irving', 'Patty Mills', 'Dante Exum', 'Matthew Dellavedova', 'Cameron Bairstow', 'Joe Ingles', 'Tyler Ennis', 'Andrew Nicholson', 'Dwight Powell', 'Ben Gordon', 'Joel Freeland', 'Steven Adams', 'Aron Baynes', 'Steve Nash', 'Anthony Bennett', 'Andrew Wiggins', 'Tristan Thompson', 'Joel Anthony', 'Nik Stauskas', 'Kelly Olynyk', 'Cory Joseph');

%data=();
my ($file1, $file2) = @ARGV;

open my $fh1, '<', $file1;
while ($line = <$fh1>){
	chomp($line);
	@vars=();
	@vars = split(/\t/, $line);
	$columns = scalar(@vars);
	if (($columns>=11) and ($vars[0] ne "RK")){
		#print "$vars[1]\t$vars[3]\t$vars[4]\t$vars[9]\n";
		$minutes = $vars[3]*$vars[4];
		$techs = $vars[9];
		$TperM = $techs/$minutes;
		$vars[1] =~ m/(.*),/g;
		$name=$1;
		if ($minutes>250){$data{$name}=$TperM;}
		#if ($minutes>250){$data{$name}=$techs;}
	}
}

@listUS=();
@listInt=();
foreach $name (sort keys %data){
	$country=0;
	if ($name ~~ @int){
		push (@listInt,$data{$name});
		$country=1;
	}
	elsif ($name ~~ @intEnglish){
		#push (@listInt,$data{$name});
		push (@listUS,$data{$name});
		$country=2;
	}
	else{
		push (@listUS,$data{$name});
	}
        #print "$name\t$data{$name}\t$country\n";
}

@listUS = sort {$a <=> $b} @listUS;
@listInt = sort {$a <=> $b} @listInt;

for ($x=0;$x<scalar(@listUS);$x++){
	if ($x<scalar(@listInt)){
		print "$listUS[$x]\t$listInt[$x]\n";
	}
	else{
		print "$listUS[$x]\n";
	}

}

exit;

#calculate percentiles. 
$third=sprintf("%.0f",(0.75*($#listUS)));
$median=sprintf("%.0f",(0.5*($#listUS)));
$first=sprintf("%.0f",(0.25*($#listUS)));
$thirdI=sprintf("%.0f",(0.75*($#listInt)));
$medianI=sprintf("%.0f",(0.5*($#listInt)));
$firstI=sprintf("%.0f",(0.25*($#listInt)));

print "#Per\tUS\tInt\n";
print "75%\t$listUS[$third]\t$listInt[$thirdI]\n";
print "50%\t$listUS[$median]\t$listInt[$medianI]\n";
print "25%\t$listUS[$first]\t$listInt[$firstI]\n";
$lUS= scalar(@listUS);
$lInt= scalar(@listInt);
print "Lengths $lUS $lInt\n";

exit;
