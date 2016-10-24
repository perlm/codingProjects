
library(ggplot2)
#library(reshape2)
#library(dygraphs)
#library(xts)
#library(googlesheets)
#library(devtools)
#library(readr)
#library(dotenv)
#library(RJDBC)

setwd("/Users/jasonperlmutter/Desktop/temp/horse")

df = read.csv("results.log",sep="\t", header=FALSE)
colnames(df) <- c('ShotProbability','WinProbability','Rounds')

ggplot(data=subset(df,ShotProbability<0.97), aes(x=as.numeric(ShotProbability), y=as.numeric(WinProbability),size=as.numeric(Rounds),color=as.numeric(Rounds))) + 
  geom_point(alpha=1.0) + xlab('Selected Shot Probability') + ylab('Win Probability') + scale_colour_continuous(name='Rounds') +
  scale_size(guide=FALSE) + ggtitle('Optimal Horse Strategy')


