options(java.parameters = "-Xmx16g")

require(ggplot2)
require(jsonlite)
require(curl)
require(lubridate)
require(reshape2)



##################
# pull data in from api
q <- paste('https://api.seatgeek.com/2/events?type=nba&per_page=1000&page=1&client_id=',
           Sys.getenv("seatgeek_client_ID"),
           '&client_secret=',
           Sys.getenv("seatgeek_secret"),sep="")

raw <- fromJSON(q)
data <- raw$events

df <- data.frame(as.Date(data$datetime_local),
                 as.numeric(as.character(unlist(data$stats$average_price))),
                 as.numeric(as.character(unlist(data$stats$listing_count))),
                 data$title
)

df$home_team <- gsub("([A-Za-z0-9 ]+).* at ([A-Za-z0-9 ]+).*", "\\2", df$data.title)
df$visiting_team <- gsub("([A-Za-z0-9 ]+).* at ([A-Za-z0-9 ]+).*", "\\1", df$data.title)

colnames(df) <- c('date','avg_price','count','game','home_team','visiting_team')
df <- subset(df,!is.na(df$count))


price <- merge(as.data.frame(xtabs(df,formula=avg_price~home_team)/xtabs(df,formula=~home_team)),
               as.data.frame(xtabs(df,formula=~home_team)), by="home_team")
colnames(price)<-c('home_team','Avg_Price','Count')
price <- subset(price,Count>1)

rawStandings <- "1,Golden State Warriors,73-9
2,San Antonio Spurs,67-15
3,Cleveland Cavaliers,57-25
4,Toronto Raptors,56-26
5,Oklahoma City Thunder,55-27
6,Los Angeles Clippers,53-29
7,Atlanta Hawks,48-34
8,Boston Celtics,48-34
9,Charlotte Hornets,48-34
10,Miami Heat,48-34
11,Indiana Pacers,45-37
12,Detroit Pistons,44-38
13,Portland Trail Blazers,44-38
14,Dallas Mavericks,42-40
15,Memphis Grizzlies,42-40
16,Chicago Bulls,42-40
17,Houston Rockets,41-41
18,Washington Wizards,41-41
19,Utah Jazz,40-42
20,Orlando Magic,35-47
21,Denver Nuggets,33-49
22,Milwaukee Bucks,33-49
23,Sacramento Kings,33-49
24,New York Knicks,32-50
25,New Orleans Pelicans,30-52
26,Minnesota Timberwolves,29-53
27,Phoenix Suns,23-59
28,Brooklyn Nets,21-61
29,Los Angeles Lakers,17-65
30,Philadelphia 76ers,10-72"
  
standings<-read.delim(textConnection(rawStandings),header=FALSE,sep=",",strip.white=TRUE)
colnames(standings) <- c('rank','home_team','winloss')
standings$wins <- as.numeric(gsub("([0-9]+)-([0-9]+)", "\\1", standings$winloss))
standings$losses <- as.numeric(gsub("([0-9]+)-([0-9]+)", "\\2", standings$winloss))
standings$winrate <- standings$wins/(standings$wins+standings$losses)

merged <- merge(price,standings,by="home_team")

ggplot(merged,aes(x=wins,y=Avg_Price)) + geom_point(size=3,alpha=0.5)+
  xlab('2015-16 Wins') + ylab('Avg Upcoming Ticket Price') +
  geom_smooth(method="lm",se=TRUE) + ggtitle('NBA Ticket Price in 2016-17 vs 2015-16 wins')

model <- glm(merged$Avg_Price~merged$wins)
summary(model)


# second question - looking into visiting golden state.

df$gsw_visiting <-ifelse(df$visiting_team=='Golden State Warriors',1,0)

nogsw <- subset(df,home_team!='Golden State Warriors')

price <- merge(merge(merge(
  as.data.frame(xtabs(subset(nogsw,gsw_visiting==0),formula=avg_price~home_team)/xtabs(subset(nogsw,gsw_visiting==0),formula=~home_team)),
  as.data.frame(xtabs(subset(nogsw,gsw_visiting==0),formula=~home_team)),by="home_team"),
  as.data.frame(xtabs(subset(nogsw,gsw_visiting==1),formula=avg_price~home_team)/xtabs(subset(nogsw,gsw_visiting==1),formula=~home_team)),by="home_team"),
  as.data.frame(xtabs(subset(nogsw,gsw_visiting==1),formula=~home_team)),by="home_team")

colnames(price) <- c('home_team','Other_visitor','num_no_gsw','GSW_visitor','num_yes_gsw')
price_2 <- melt(price, id.vars=c("home_team"),measure.vars=c("Other_visitor","GSW_visitor"))


ggplot(price_2,aes(x=home_team,y=value,color=variable)) + geom_point(size=4,alpha=0.5)+
  xlab('NBA Team') + ylab('Avg Upcoming Ticket Price') +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  ggtitle('Ticket price when GSW visits') + 
  scale_color_discrete('')


mean(price$Other_visitor)
mean(price$GSW_visitor)