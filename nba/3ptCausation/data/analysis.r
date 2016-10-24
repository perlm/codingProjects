
setwd("~/Desktop/Dropbox/personal/nba/3ptCausation/data")
data = read.csv("teamStats.data")

#cor.test(data$FG3A,data$WPCT)
print("this works")

line <- lm(data$WPCT ~ data$FG3A)
print(summary(line))
plot(data$FG3A,data$WPCT,main='3-Attempts and Winning',xlab='3-Attempts per Game',ylab='Season Winning %',pch=19,col='blue')
abline(line,col='red',lwd=3)

lineAll <- lm(data$WPCT ~ data$FG3A+data$FG2PCT+data$FTM+data$OREB+data$DREB+data$AST+data$TOV+data$STL+data$BLK+data$BLKA+data$PF)
print(summary(lineAll))

forPairs = data[,c("WPCT","FG3A","FGPCT","PTS")]
pairs(forPairs)


