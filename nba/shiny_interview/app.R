library(shiny)
#library(ggplot2)
library(reshape2)
library(dygraphs)
library(xts)
library(devtools)
library(rsconnect)

# I did this for an interview with the nba on march 4 2016.

# to deploy - type:  rsconnect::deployApp('/home/jason/Desktop/Dropbox/personal/nba/shiny_interview/')

#setwd("/home/jason/Desktop/Dropbox/personal/nba/shiny_interview")

df2 = read.table("Questionnaire Dataset (Per Game Stats as of Jan 29 2016).csv", header=TRUE, sep=",", quote='"', nrows=1000000)
df2$year <- as.Date(paste(substr(df2$Season,0,4),"01", "01",sep="-"),format="%Y-%m-%d")
#df2$inches <- 12*as.numeric(substr(df2$Height,0,1)) +as.numeric(substr(df2$Height,3,4))

#df3 <- data.frame(aggregate(df2$X3PM, list(team=df2$Team,year=df2$year), sum))
df3 <- data.frame(aggregate(cbind(df2$AST,df2$X3PM,df2$Small), list(team=df2$Team,year=df2$year), sum))
colnames(df3) <- c("team","year","AST","X3PM","Small")
  
#assists
glm(formula=df3$X3PM~df3$AST)
cor(df3$AST,df3$X3PM)
#ggplot() + geom_point(data=df3, aes(x=as.numeric(AST), y=as.numeric(X3PM),color=as.factor(team)),alpha=0.5,size=5)+ scale_colour_discrete(guide = FALSE)+xlab("Team Assists per Game") + ylab("3-pt Made per Game")+ geom_abline(intercept=2.33,slope=0.238)
  
#small-ball
df <- dcast(df3,year~team, value.var="Small")
ts <- as.xts(df[,-1], order.by=as.Date(df$year))
#dygraph(ts,main="Minutes for Players <= 6'6'' ") %>% dyHighlight(highlightSeriesBackgroundAlpha = 0.5, highlightCircleSize = 0, highlightSeriesOpts = list(strokeWidth = 5),hideOnMouseOut = FALSE) %>% dyLegend(show = "onmouseover") 


# 3-pt
df <- dcast(df3,year~team, value.var="X3PM")
ts <- as.xts(df[,-1], order.by=as.Date(df$year))
d1 <- dygraph(ts,main="3-pt Made per Game") %>% dyHighlight(highlightSeriesBackgroundAlpha = 0.5, highlightCircleSize = 0, highlightSeriesOpts = list(strokeWidth = 5),hideOnMouseOut = FALSE) %>% dyLegend(show = "onmouseover") 
d1$x$css = ".dygraph-legend > span {display:none;}
  .dygraph-legend > span.highlight { display: inline; }"
d1


ui <- shinyUI(fluidPage(
  titlePanel("3-pt Made per Game"),
  dygraphOutput("dygraph")
))


server <- shinyServer(function(input, output) {
  d1 <- dygraph(ts,main="3-pt Made per Game") %>% 
    dyHighlight(highlightSeriesBackgroundAlpha = 0.5, highlightCircleSize = 0, highlightSeriesOpts = list(strokeWidth = 5),hideOnMouseOut = FALSE) %>%     dyLegend(show = "onmouseover") %>% dyAxis("x", axisLabelFormatter = "function(d){ return d.getFullYear() }")
  d1$x$css = ".dygraph-legend > span {display:none;}
  .dygraph-legend > span.highlight { display: inline; }"
  output$dygraph <- renderDygraph({d1})
})

shinyApp(ui = ui, server = server)

