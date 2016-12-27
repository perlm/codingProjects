options(java.parameters = "-Xmx16g")

require(ggplot2)

setwd('/home/jason/Dropbox/gitHubable/philosophy/analysis')

df <- read.csv('wisdom.data',header = FALSE,sep = ",")

colnames(df) <- c('book_id','Title','Author','Year','Wisdom')
ggplot(df,aes(x=as.numeric(as.character(Year)),y=1000*as.numeric(as.character(Wisdom))))+
  geom_point(size=3,alpha=0.75)+
  xlab('Year') + ylab('Wisdom/1000 Words') + geom_smooth()

ggplot(df,aes(x=1000*as.numeric(as.character(Wisdom))))+
  geom_histogram(binwidth=0.1)+
  xlab('Wisdom/1000 Words')
