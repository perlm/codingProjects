
######
# Jeopary Model
# Goal is to predict probability that returning champ will win match on jeopardy given the information in the Jeopardy archive.
# http://j-archive.com/
########

setwd("/home/jason/Desktop/Dropbox/personal/jeopardy/predicting")

library(ROCR)
library(ggplot2)
library(glmnet)
library(dygraphs)
library(xts)
library(reshape2)


calc_AUC <- function(obs, pred, plotROC=FALSE) {
  roc.pred<-prediction(pred, obs)
  if (plotROC) {
    roc.perf <- performance(roc.pred, measure="tpr", x.measure="fpr")
    plot(roc.perf)
    abline(a=0,b=1)
  }
  return(performance(roc.pred, "auc")@y.values[[1]])
}

df = read.table("raw.data", header=FALSE, sep=",", quote='', nrows=250000)
colnames(df) <- c("index", "gameID","date","ConsecutiveWins","TotalDollars","Outcome","Gender","Age","Name","Occuppation","Location")

# convert outcome to zero/one
df$Outcome[df$Outcome==2]<-0

#try restructuring data
df$ave <- df$TotalDollars/df$ConsecutiveWins

df$TotalDollars_buckets[df$TotalDollars<=15000] <- 'lt15k'
df$TotalDollars_buckets[df$TotalDollars>15000 & df$TotalDollars<=35000] <- '15-35k'
df$TotalDollars_buckets[df$TotalDollars>35000 & df$TotalDollars<=75000] <- '35-75k'
df$TotalDollars_buckets[df$TotalDollars>75000 & df$TotalDollars<=150000] <- '75-150k'
df$TotalDollars_buckets[df$TotalDollars>150000] <- 'gt150k'

df$age_bucket[df$Age<=25] <- 'lt25'
df$age_bucket[df$Age>25 & df$Age<=35] <- '25-35'
df$age_bucket[df$Age>35 & df$Age<=45] <- '35-45'
df$age_bucket[df$Age>45 & df$Age<=55] <- '45-55'
df$age_bucket[df$Age>55] <- 'gt55'

df$TotalDollars_buckets <- as.factor(df$TotalDollars_buckets)
df$age_bucket <- as.factor(df$age_bucket)

df$ConsecutiveWins[df$ConsecutiveWins>=10]<-10
df$ConsecutiveWins <- as.factor(df$ConsecutiveWins)
df$ConsecutiveWins <- as.numeric(df$ConsecutiveWins)

df$date <- as.Date(df$date)

# Examine data
mean(as.numeric(df$Outcome))
aggregate(df$Outcome, list(Condition=df$ConsecutiveWins), length)
aggregate(df$Outcome, list(Condition=df$ConsecutiveWins), mean)
aggregate(df$Outcome, list(Condition=df$TotalDollars), length)
aggregate(df$Outcome, list(Condition=df$TotalDollars), mean)
aggregate(df$Outcome, list(Condition=df$TotalDollars_buckets), length)
aggregate(df$Outcome, list(Condition=df$TotalDollars_buckets), mean)
aggregate(df$Outcome, list(Condition=df$age_bucket), length)
aggregate(df$Outcome, list(Condition=df$age_bucket), mean)


#simplify data frame and setup for training  
r <- names(df) %in% c('index','gameID','date','Name','pred')
to <- df[!r]
sapply(to,function(x)length(levels(as.factor(x))))
bad <- sapply(to,function(x)length(levels(as.factor(x)))<2)
to <- to[!bad]

to$holdout <- runif(nrow(to)) > 0.7
train.data <- to[!to$holdout, ]
validate.data <- to[to$holdout, ]

# model formula
f <- formula(Outcome ~ ConsecutiveWins + TotalDollars_buckets  + Gender + age_bucket +
               ConsecutiveWins:TotalDollars_buckets + 
               #age_bucket:Gender + ConsecutiveWins:Gender +
               poly(ConsecutiveWins,3),data=to)

mm <- sparse.model.matrix(f, data=train.data)
cvmn <- cv.glmnet(mm[,-1], train.data$Outcome, family="binomial", standardize=TRUE, nlambda=50, 
                  type.measure="auc", nfold=5,maxit=10000)
plot(cvmn)

coef(cvmn, s=cvmn$lambda.min)    #model coefficients for lambda which minimizes error.
calc_AUC(train.data$Outcome, predict(cvmn, newx=mm[,-1], type="response", s = "lambda.min"), "TRUE")
#in-sample AUC 0.61

# predict for holdout
mm <- model.matrix(f, data=validate.data)
calc_AUC(validate.data$Outcome, predict(cvmn, newx=mm[,-1], type="response", s = "lambda.min"), "FALSE")
#out-of-sample AUC 0.58

# predict for whole set
mm <- model.matrix(f, data=df)
df$pred <- predict(cvmn, newx=mm[,-1], type="response", s = "lambda.min")


# Visualize
ggplot(data=df,aes(pred))+geom_histogram(bins=10)+xlab('Predicted Probability')+ggtitle('Distribution of Predictions')
ggplot(data=df,aes(pred,fill=as.factor(TotalDollars_buckets)))+geom_histogram(binwidth=0.05,position="dodge")+xlab('Predicted Probability')+ggtitle('Distribution of Predictions')

ggplot(data=df,aes(x=date,y=pred,color=Name))+ggtitle('30 Years of Jeopardy!')+
  geom_line(size=1,alpha=0.75) + xlab('Date') + ylab('Predicted Win Prob')+scale_colour_discrete(guide=FALSE)


ts <- as.xts(df[c('date','Name','pred')], order.by=as.Date(df[c('date','Name','pred')]$date))
dygraph(ts,main="Model Prediction over Time") %>% dyHighlight(highlightSeriesBackgroundAlpha = 0.5, highlightCircleSize = 5, highlightSeriesOpts = list(strokeWidth = 1),hideOnMouseOut = FALSE) %>% dyLegend(show = "onmouseover") 


       



