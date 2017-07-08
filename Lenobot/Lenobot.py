#!/usr/bin/python

# I put this on google app engine several years ago....
from google.appengine.api import urlfetch
import urllib
import urllib2
import re
import sys
import cgi
import cgitb
import random
cgitb.enable()


print "Content-Type: text/html\n\n"

def generate_form(search, rhyme):
	print "<HTML>\n"
	print "<HEAD>\n"
	print "\t<TITLE>Leno-Bot</TITLE>\n"
	print "</HEAD>\n"
	print "<BODY BGCOLOR = white>\n"
	
	print "\t<H1>So what's trending on Google right now?</H1>\n"
	print "\t<H1>Have you of heard about this? This is true.</H1>\n"
	words =  search.split(" ")
	length = len(words)
	
	if length < 2:
		print "\t<H1>"+ search + "? More like", rhyme + "!</H1>\n"
	else:
		length = length - 1
		these = words[0:length]
		cat = " ".join(these)
		print "\t<H1>"+ search + "? More like", cat + "-" + rhyme + "!</H1>\n"
	print "<br>Not very funny? What do you expect from a script which takes a top "
	print '<a href="http://www.google.com/trends">trending google search</a>'  
	print "and enters it into a "
	print '<a href="http://www.rhymezone.com">rhyming dictionary</a>'
	print "? It's not like Leno's so great.\n"
	print "Just reload the page, so we can get on with the show.\n"
	print "</BODY>\n"
	print "</HTML>\n"


def main():
	web = "http://www.google.com/trends/"

	temp = urlfetch.fetch(web, follow_redirects=False, deadline=10)
	esearch_result = temp.content
	#esearch_result =urllib.urlopen(web).read()

	lines = []
	lines = esearch_result.split("\n")
	trends = []
	match = "hottrends?q"
	for line in lines:
		if match in line:
			trend = re.search('(?<=\?q=).*(?=&date)',line)
			trend = trend.group(0).replace("+", " ")
			trends.append(trend)
	
	length = len(trends) -1
	rand = random.randint(0,length)	
	search = trends[rand]
	
	#search = trends[0]		
	words =  search.split(" ")		
	web= "http://www.rhymezone.com/r/rhyme.cgi?Word=" + words[-1] + "&typeofrhyme=nry&org1=syl&org2=l&org3=y"
	temp = urlfetch.fetch(web, follow_redirects=False, deadline=10)
	esearch_result = temp.content
	#esearch_result =urllib.urlopen(web).read()

	web= "http://www.rhymezone.com/r/rhyme.cgi?Word=" + words[-1] + "&typeofrhyme=perfect&org1=syl&org2=l&org3=y"
	temp2 = urlfetch.fetch(web, follow_redirects=False, deadline=10)
	esearch_result = esearch_result + temp2.content
	
	lines = []
	lines = esearch_result.split("\n")
	rhymes = []
	#match = "d?u"	#Itlooks like rhymezone changed, so I have to change the match term 1/8/2012
	match = 'A HREF="d='
	for line in lines:
		#print line
		if match in line:
			#print line
			rhyme = re.search('(?<=\">).*(?=</A>)',line)
			rhyme = rhyme.group(0).replace("&nbsp;", " ")
			rhymes.append(rhyme)

	length = len(rhymes)-1
	if length>=0:
		rand = random.randint(0,length)	
		rhyme = rhymes[rand]
	else:
		rhyme = "orange"
	#print search, rhyme
	generate_form(search, rhyme)
	
main()
