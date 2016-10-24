#!/usr/bin/perl

@lines=<STDIN>;

$max=0;
for $line (@lines)
{
        chomp($line);
	$l = length($line);
	if ($l>$max)
	{
	$max=$l;
	}
}

for $line (@lines)
{
        chomp($line);
	$l = length($line);
	if ($l>=$max)
	{
	print "$line\n"
	}
}

