# ---- setup ----
  
options(java.parameters = "-Xmx16g")
suppressMessages(library(ROCR, warn.conflicts = FALSE, quietly=TRUE))
suppressMessages(library(RJDBC, warn.conflicts = FALSE, quietly=TRUE))
suppressMessages(library(ggplot2, warn.conflicts = FALSE, quietly=TRUE))
suppressMessages(library(reshape2, warn.conflicts = FALSE, quietly=TRUE))
suppressMessages(library(Hmisc, warn.conflicts = FALSE, quietly=TRUE))
suppressMessages(library(dotenv, warn.conflicts = FALSE, quietly=TRUE))
suppressMessages(library(knitr, warn.conflicts = FALSE, quietly=TRUE))
suppressMessages(library(lubridate, warn.conflicts = FALSE, quietly=TRUE))
suppressMessages(library(maps, warn.conflicts = FALSE, quietly=TRUE))
suppressMessages(library(glmnet, warn.conflicts = FALSE, quietly=TRUE))

# data from:
# http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time

setwd('/Users/jasonperlmutter/Desktop/temp/other_project')

# load in some csv's
df <- data.frame(DAY_OF_WEEK=character(),FL_DATE=character(),CARRIER=character(),ORIGIN=numeric(),DEST=numeric(),ARR_DELAY_NEW=numeric(),ACTUAL_ELAPSED_TIME=numeric())
files <- Sys.glob('2015/*.csv')
for (file in files){
  temp <- read.csv(file,header = TRUE,sep = ",")
  df <- rbind(df, temp)
}
df$X<-NULL
df$FL_DATE <- as.Date(df$FL_DATE)

# define late as >15 minutes post scheduled arrival.
df$delayed <- ifelse(df$ARR_DELAY_NEW>15,1,0)

# convert dow & month to characters
df$dow <- factor(df$DAY_OF_WEEK, labels = c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"), ordered = TRUE)
df$month <- month(df$FL_DATE)
df$month_word <- factor(df$month, labels = c('January','February','March','April','May','June','July','August','September','October','November','December'),ordered = TRUE)

# airport dictionary
airports <- read.csv('airports.csv',header = TRUE,sep = ",")
df <- merge(df,airports,by.y="iata",by.x="ORIGIN")
df <- merge(df,airports,by.y="iata",by.x="DEST")

# carrier dictionary
carriers <- read.csv('carriers.csv',header = TRUE,sep = ",")
carriers <- carriers[!carriers$Code=="", ]
df <- merge(df,carriers,by.y="Code",by.x="CARRIER")

colnames(df)<-c("CARRIER","DEST","ORIGIN","DAY_OF_WEEK","FL_DATE","ARR_DELAY_NEW","ACTUAL_ELAPSED_TIME",
  "delayed","dow","month","month_word",
  "Origin_Airport","Origin_City","Origin_State","Origin_Country", "Origin_lat","Origin_long",
  "Dest_Airport","Dest_City","Dest_State","Dest_Country", "Dest_lat","Dest_long",
  "Airline")
df$Airline <- as.character(df$Airline)
df$Airline[df$Airline=='US Airways Inc. (Merged with America West 9/05. Reporting for both starting 10/07.)'] <- 'US Airways Inc.'

# remove na's 
df2 <- na.omit(df)


# ---- frequency ----

# What is the distribution of flights in the data set?
a <- as.data.frame(xtabs(df2,formula=~dow)/xtabs(df2[!duplicated(df2$FL_DATE),],formula=~dow))
colnames(a)<-c('Day of Week','Avg Number of Flights Per Day')

b <- as.data.frame(xtabs(df2,formula=~month_word)/xtabs(df2[!duplicated(df2$FL_DATE),],formula=~month_word))
colnames(b)<-c('Month','Avg Number of Flights Per Day')

c <- as.data.frame(xtabs(df2,formula=~Airline)/nrow(df2[!duplicated(df2$FL_DATE),]))
c <- c[order(-c$Freq),]
c <- subset(c,Freq>0)
c<-c[1:10,]
colnames(c)<-c('Carrier','Avg Number of Flights Per Day')

# Sanity check--- Rate planes arrive should equal rate planes depart. 
d <- merge(
  as.data.frame(xtabs(df2,formula=~Origin_Airport)/nrow(df2[!duplicated(df2$FL_DATE),])),
  as.data.frame(xtabs(df2,formula=~Dest_Airport)/nrow(df2[!duplicated(df2$FL_DATE),])),
  by.x="Origin_Airport",by.y="Dest_Airport")
d$total <- d$Freq.x+d$Freq.y
d <- d[order(-d$total),]
d <- d[1:10,]
colnames(d)<-c('Airport','Avg Departing Per Day','Avg Arrive Per Day','Total Flights Per Day')

kable(a,digits=0, caption='Flights by Day of week',row.names=FALSE)
kable(b,digits=0, caption='Flights by Month',row.names=FALSE)
kable(c,digits=0, caption='Flights by Airline',row.names=FALSE)
kable(d[,c(1,4)],digits=0, caption='Flights by Airport',row.names=FALSE)


# ---- frequency_plot ----
#just plot by date, for fun.
#plots <- list()
#plots[[1]] <- 
ggplot(data=df2, aes(x=FL_DATE)) + geom_freqpoly(binwidth=1,size=2)+
  xlab('Date') + ylab('Number of Flights') + xlim(c(as.Date('2015-01-02'),as.Date('2015-12-31'))) +
  ggtitle('Number of Flights by Date') + 
  geom_vline(xintercept = as.numeric(as.Date(c('2015-12-25','2015-11-26','2015-01-19','2015-06-03','2015-05-25','2015-09-07','2015-02-16'))), linetype=1, color="blue") 
#ggplot(data=df2, aes(x=month_word)) + geom_histogram(alpha=0.75) + ylab('Number of Flights')  + xlab('Month')
#ggplot(data=b, aes(x=DAY_OF_WEEK,y=Freq)) + geom_bar(stat="identity",alpha=0.75) + ylab('Number of Flights')  + xlab('Day of Week')
#multiplot(plotlist = plots, cols=1)


# ---- lateness ----

# What is the distribution of flights in the data set?
a <- as.data.frame(xtabs(df2,formula=delayed~dow)/xtabs(df2,formula=~dow))
colnames(a)<-c('Day of Week','Delay Rate')

b <- as.data.frame(xtabs(df2,formula=delayed~month_word)/xtabs(df2,formula=~month_word))
colnames(b)<-c('Month','Delay Rate')

c <- as.data.frame(xtabs(df2,formula=delayed~Airline)/xtabs(df2,formula=~Airline))
c <- c[order(-c$Freq),]
c <- subset(c,Freq>0)
colnames(c)<-c('Carrier','Delay Rate')

d <- merge(
  as.data.frame(xtabs(df2,formula=delayed~Origin_Airport)/xtabs(df2,formula=~Origin_Airport)),
  as.data.frame(xtabs(df2,formula=delayed~Dest_Airport)/xtabs(df2,formula=~Dest_Airport)),
  by.x="Origin_Airport",by.y="Dest_Airport")
#assume no net movement of planes
d$total <- (d$Freq.x+d$Freq.y)/2
d <- d[order(-d$total),]
d <- d[1:10,]
colnames(d)<-c('Airport','Departing Delay Rate','Arriving Delay Rate','Avg Delay Rate')

kable(a,digits=2, caption='Delayed by Day of week',row.names=FALSE)
kable(b,digits=2, caption='Delayed by Month',row.names=FALSE)
kable(c,digits=2, caption='Delayed by Airline',row.names=FALSE)
kable(d,digits=2, caption='Delayed by Airport',row.names=FALSE)


# ---- lateness_plot ----
#just show one plot for fun
#plots <- list()
#plots[[1]] <- 
ggplot(data=df2, aes(x=FL_DATE,y=delayed)) +
  stat_summary(fun.y="mean", geom="line", size=2) +  xlab('Date') + ylab('Fraction Delayed') + 
  xlim(c(as.Date('2015-01-02'),as.Date('2015-12-31'))) +  
  geom_vline(xintercept = as.numeric(as.Date(c('2015-12-25','2015-11-26','2015-01-19','2015-06-03','2015-05-25','2015-09-07','2015-02-16'))), linetype=1, color="blue") +
  ggtitle('Delay Rate by Date') 
#plots[[2]] <- ggplot(data=df2, aes(x=month_word,y=delayed)) + stat_summary(fun.y="mean", geom="point", size=5)+  ylab('Fraction Delayed')  + xlab('Month')
#plots[[3]] <- ggplot(data=df2, aes(x=dow,y=delayed)) + stat_summary(fun.y="mean", geom="point", size=5)+  ylab('Fraction Delayed') +xlab('Day of Week')
#multiplot(plotlist = plots, cols=1)

######################################
#Quick statistical test! 
#aovtest <- aov(delayed ~ dow, data=df2)
#kable(summary(aovtest),title='AOV')
#TukeyHSD(aovtest)
######################################


# ---- model ----
# for a bit of fun--- make a model!

df2$dow<-factor(df2$dow,ordered = FALSE)
df2$month_word<-factor(df2$month_word,ordered = FALSE)

# make a holdout and use CV.
df2$holdout <- runif(nrow(df2)) > 0.25
train.data <- df2[!df2$holdout, ]
validate.data <- df2[df2$holdout, ]


# instead of using airport as a factor (since there're so many of them), create a continuous variable using training set.
a <- as.data.frame(xtabs(train.data,formula=delayed~ORIGIN)/xtabs(train.data,formula=~ORIGIN))
b <- as.data.frame(xtabs(train.data,formula=delayed~DEST)/xtabs(train.data,formula=~DEST))
# mean impute
a$Freq[is.na(a$Freq)] = mean(a$Freq, na.rm=TRUE)
b$Freq[is.na(b$Freq)] = mean(b$Freq, na.rm=TRUE)
colnames(a) <- c('ORIGIN','Origin_delay_rate')
colnames(b) <- c('DEST','Dest_delay_rate')

train.data <- merge(train.data,a,by="ORIGIN")
train.data <- merge(train.data,b,by="DEST")

f <- formula(delayed ~ Dest_delay_rate + Origin_delay_rate + Airline + dow + month_word)
mm <- sparse.model.matrix(f, data=train.data)
cvmn <- cv.glmnet(mm[,-1], train.data$delayed, family="binomial", alpha=1,
                  standardize=TRUE, type.measure="auc", nfold=10,nlambda=10,maxit=10000)
# plot(cvmn)

coef <- suppressMessages(coef(cvmn, s=cvmn$lambda.1se)[order(abs(coef(cvmn, s=cvmn$lambda.1se)), decreasing = TRUE)][1:41])
names <- suppressMessages(rownames(coef(cvmn, s=cvmn$lambda.1se))[order(abs(coef(cvmn, s=cvmn$lambda.1se)), decreasing = TRUE)][1:41])
all <- data.frame(cbind(names,coef))
colnames(all) <- c('Feature Name','Coefficients')
all$Coefficients <- as.numeric(as.character(all$Coefficients))
kable(na.omit(all),digits=3,caption='Model Coefficients')

# ---- model_plot ----
# use training set rates in prediction.
validate.data <- merge(validate.data,a,by="ORIGIN")
validate.data <- merge(validate.data,b,by="DEST")
mm <- model.matrix(f, data=validate.data)
validate.data$prediction <- predict(cvmn, newx=mm[,-1], type="response", s = "lambda.1se")[,1]

auc <- calc_AUC(validate.data$delayed, validate.data$prediction, "FALSE")

a <- as.data.frame(xtabs(validate.data,formula=delayed~round(prediction,2))/xtabs(validate.data,formula=~round(prediction,2)))

plots <- list()
plots[[1]] <- ggplot(a,aes(x=as.numeric(as.character(round.prediction..2.)),y=Freq)) + geom_point(size=3,alpha=0.75)+geom_abline(intercept=0,slope=1)+
  xlab('Predicted Delay Rate')+ylab('Actual Delay Rate') +
  ggtitle(paste("Holdout Calibration Analysis, AUC=",round(auc,3),sep=""))+ xlim(c(0,0.4)) + ylim(c(0,0.4))
plots[[2]] <- ggplot(validate.data,aes(prediction,fill=Airline)) + geom_histogram(alpha=0.75,binwidth=0.01)+
  xlab('Predicted Delay Rate')+ ggtitle('Distribution of Predicted Rates')+ xlim(c(0,0.4))
multiplot(plotlist = plots, cols=1)


# ---- geo ----

# to calculate distance
radians<-function(arg1){
  r<-arg1*pi/180
  return(r)
}

#e$distance <- 3959*acos(cos(radians(e$lat.x))*cos(radians(e$lat.y))*cos(radians(e$long.y) - radians(e$long.x)) + sin(radians(e$lat.x))*sin(radians(e$lat.y)))
usa <- map_data("usa")

a <- aggregate(df2$delayed, list(df2$ORIGIN,df2$DEST), length)
colnames(a) <- c("ORIGIN","DEST","Count")
b <- merge(merge(a,airports,by.y="iata",by.x="ORIGIN"),airports,by.y="iata",by.x="DEST")

c <- as.data.frame(xtabs(df2,formula= ~ORIGIN))
d <- as.data.frame(xtabs(df2,formula= delayed~ORIGIN)/xtabs(df2,formula= ~ORIGIN))
e <- merge(merge(c,d,by="ORIGIN"),airports,by.y="iata",by.x="ORIGIN")

# calc fractions
# nrow(subset(df2,Origin_Airport %in% c('William B Hartsfield-Atlanta Intl','Chicago O\'Hare International','Dallas-Fort Worth International','Denver Intl','Los Angeles International','San Francisco International','Phoenix Sky Harbor International','George Bush Intercontinental','McCarran International','Minneapolis-St Paul Intl')|Dest_Airport %in% c('William B Hartsfield-Atlanta Intl','Chicago O\'Hare International','Dallas-Fort Worth International','Denver Intl','Los Angeles International','San Francisco International','Phoenix Sky Harbor International','George Bush Intercontinental','McCarran International','Minneapolis-St Paul Intl')))/nrow(df2)
# nrow(subset(df2,Origin_Airport %in% c('William B Hartsfield-Atlanta Intl','Chicago O\'Hare International','Dallas-Fort Worth International','Denver Intl','Los Angeles International','San Francisco International','Phoenix Sky Harbor International','George Bush Intercontinental','McCarran International','Minneapolis-St Paul Intl')|Dest_Airport %in% c('William B Hartsfield-Atlanta Intl','Chicago O\'Hare International','Dallas-Fort Worth International','Denver Intl','Los Angeles International')))/nrow(df2)

# cutting off AK/HI/PR
b$airport.x<-as.character(b$airport.x)
b$airport.y<-as.character(b$airport.y)

#b$airport_color <- ifelse(b$airport.x %in% c('William B Hartsfield-Atlanta Intl','Chicago O\'Hare International','Dallas-Fort Worth International','Denver Intl','Los Angeles International','San Francisco International','Phoenix Sky Harbor International','George Bush Intercontinental','McCarran International','Minneapolis-St Paul Intl'),b$airport.x,(ifelse(b$airport.y %in% c('William B Hartsfield-Atlanta Intl','Chicago O\'Hare International','Dallas-Fort Worth International','Denver Intl','Los Angeles International','San Francisco International','Phoenix Sky Harbor International','George Bush Intercontinental','McCarran International','Minneapolis-St Paul Intl'),b$airport.y,'other')))
b$airport_color <- ifelse(b$airport.x %in% c('William B Hartsfield-Atlanta Intl','Chicago O\'Hare International','Dallas-Fort Worth International','Denver Intl','Los Angeles International'),b$airport.x,(ifelse(b$airport.y %in% c('William B Hartsfield-Atlanta Intl','Chicago O\'Hare International','Dallas-Fort Worth International','Denver Intl','Los Angeles International'),b$airport.y,'other')))


plots <- list()
plots[[1]] <- ggplot() + 
  geom_polygon(data = usa, aes(x=long, y = lat, group = group),fill = NA, color = "black") + coord_fixed(1.3) +
  geom_point(data=e,aes(x=long,y=lat,size=Freq.x,color=Freq.y),alpha=0.75) + 
  xlab('Longitude') + ylab('Latitude') + scale_size(range=c(1,10),guide='none') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_blank(), axis.line = element_blank()) + 
  xlim(c(-125,-65)) + ylim(c(25,55)) + 
  scale_color_gradient(name='Delay Rate',limits=c(0.15, 0.25), low="red")
plots[[2]] <-  ggplot() + 
  geom_polygon(data = usa, aes(x=long, y = lat, group = group),fill = NA, color = "black") + coord_fixed(1.3) +
  geom_segment(data=subset(b,airport_color!='other'),aes(x=long.x,y=lat.x,xend=long.y,yend=lat.y,size=Count,color=airport_color),alpha=0.2) + 
  xlab('Longitude') + ylab('Latitude') + scale_size(range=c(0.1,3),guide='none') +
  guides(colour = guide_legend(title='Airport',override.aes = list(size=5,alpha=1))) +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_blank(), axis.line = element_blank()) + 
  xlim(c(-125,-65)) + ylim(c(25,55))
multiplot(plotlist = plots, cols=1)

