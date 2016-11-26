# -*- coding: utf-8 -*-

import string, time, re, os, sys,datetime


def predict(**kwargs):
        #{'date':date,'days':winningDays,'dollars':winningDollars,'gender':gender,'age':age,'name':name,'career':career,'location':location}

	# coefficients
	#(Intercept)                                        -1.021001e+00
	#ConsecutiveWins_capped                              1.147054e-01
	#Avg_Dollars                                         1.446687e-05
	#GenderM                                             3.364324e-01
	#GenderU                                             3.563753e-01
	#age_bucketb_35-55                                  -7.455324e-02
	#age_bucketc_gt55                                   -7.763322e-02
	#cityofchampionselse                                -9.250726e-02
	#jobslaw                                            -8.807188e-02
	#jobsother                                           .           
	#jobsstudent                                         2.042046e-01
	#jobsteacher                                        -9.026486e-02
	#jobstech                                            .           
	#jobswriter                                          2.056613e-01
	#year_relative                                       2.242525e-02
	#ConsecutiveWins_capped:Avg_Dollars_bucketsb_10-30k  4.249614e-02
	#ConsecutiveWins_capped:Avg_Dollars_bucketsc_gt30k   1.839559e-01


	#add in constructed variables
	kwargs['ConsecutiveWins_capped']	= min(kwargs['days'],10)
	kwargs['Avg_Dollars']			= kwargs['dollars']/kwargs['days']
	if kwargs['age']>35 and kwargs['age']<=55:age_bucket 	= 'b_35-55'
	elif kwargs['age']>55:age_bucket			= 'c_gt55'		

	if kwargs['location'] in ('Los Angeles California','Washington D.C.','Chicago Illinois','New York New York','Brooklyn New York','Arlington Virginia','Seattle Washington','New York City New York','Atlanta Georgia','San Diego California','Austin Texas','Philadelphia Pennsylvania','San Francisco California','Minneapolis Minnesota','Boston Massachusetts','Denver Colorado','Houston Texas','Baltimore Maryland','New Orleans Louisiana','Louisville Kentucky'):
		kwargs['cityofchampions']='championcity'
	else:kwargs['cityofchampions']='else'

	kwargs['year_relative']=2017-2016

# need regex for this part...
#df$jobs<-'other'
#df$jobs[grep(paste(lawjobs,collapse="|"),df$Occuppation,value=FALSE)]<-'law'
#df$jobs[grep("student|Ph.D. candidate",df$Occuppation,value=FALSE)]<-'student'
#df$jobs[grep("writer",df$Occuppation,value=FALSE)]<-'writer'
#df$jobs[grep("home",df$Occuppation,value=FALSE)]<-'home'
#df$jobs[grep("teach|professor|college instructor|librarian",df$Occuppation,value=FALSE)]<-'teacher'
#df$jobs[grep("engineer|scien|software|programmer",df$Occuppation,value=FALSE)]<-'tech'

	# construct the function!
	



if __name__ == '__main__':
	print predict()


