library(dplyr)
library(ggplot2)

# set wd
#setwd("~/OneDrive/Portfolio/recipes")
setwd("C:/Users/remme/OneDrive/Portfolio/recipes")

gg_monthly_meals <- function(dates, cats, meals
                             ,fill_colors, missing_dates = FALSE) {
  # for missing values, NAs, provide color as gray87
  cols<-append(fill_colors, c("NAs" = "gray87"), length(fill_colors))
  # organize in a dataframe
  df<-data.frame(dates,cats,meals)
  # month names in order
  months <- c('January','February','March','April','May','June'
              ,'July','August','September','October','November','December')
  
  # Do we want Missing Dates?
  if (missing_dates == TRUE) {
    mindate <- min(dates)
    maxdate <- max(dates)
    timeframe <- seq(mindate, maxdate, by="1 day")
  } else{
    timeframe <- df$dates
  }

  tbl0<-data.frame(timeframe) %>%
          left_join(df, by =c('timeframe'='dates'))%>%
          # Day of Week, Week Num, Day in Month, Day Name
          mutate(dow = as.numeric(format(timeframe, "%w"))) %>%
          mutate(week = as.numeric(format(timeframe, "%U"))) %>%
          mutate(days = as.numeric(format(timeframe, "%d"))) %>%
          mutate(day_name = weekdays(timeframe))%>%
          mutate(month = format(timeframe, "%B")) %>%
          mutate(month = factor(month, levels=months, ordered=TRUE)) %>%
          mutate(month_week = week-min(week)) %>%
          mutate(y = max(month_week)-month_week)
    
  # fix missing categories
  tbl0$cats<-tbl0$cats%>%
    as.character(tbl0$cats)%>%
    replace(is.na(.), 'NAs')
  
  # fix missing meals
  tbl0$meals<-tbl0$meals%>%
          as.character(tbl0$cats)%>%
          replace(is.na(.), '')
  
  lcats<-unique(tbl0$cats)
  lcats<-lcats[!lcats%in%c('NAs')]
  lcats<-factor(lcats,levels = lcats)
  
  name<-c('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')
  name<-factor(name, levels = name, ordered = TRUE)
  name<-name[name%in%tbl0$day_name]
  
  ggplot() +
    geom_tile(aes(dow, y, fill = cats), tbl0, color='black') +
    geom_text(aes(dow, y, label = meals), tbl0, size=3) +
    geom_text(aes(x=dow, y = y+.40, label = days), tbl0, size=3) +
    facet_wrap(~month, ncol=4, scales='free') +
    scale_x_continuous(expand=c(0,0), position='top',
                       breaks=seq(min(tbl0$dow),max(tbl0$dow)), labels=name) +
    scale_y_continuous(expand=c(0,0)) +
    scale_fill_manual(breaks = levels(lcats),values=cols) + 
    theme(
      panel.background=element_rect(fill=NA, color=NA)
      ,strip.background = element_rect(fill=NA, color=NA)
      ,strip.text.x = element_text(face="bold",color='black',size=12)
      ,legend.title = element_blank()
      ,legend.text = element_text(size = 15)
      ,axis.ticks=element_blank()
      ,axis.title=element_blank()
      ,axis.text.y = element_blank()
      ,axis.text.x = element_text(color='black',size=10)
      ,legend.position = 'bottom'
      ,strip.placement = 'outsite'
    )
}

df<-read.csv('output/meals.csv')
df$dates<-as.Date(df$dates)
df<-df[df$Category!='Off',]
dates <- df$dates
cats <- as.character(df$Category)
meals <- as.character(df$Meals)
fill_colors <- c("Chicken" = "goldenrod1"
            ,"Fish" = "darkslategray3"
            ,"Meat" = "violetred1"
          )
p<-gg_monthly_meals(dates, cats, meals, fill_colors,TRUE)
p
ggsave('figs/calendar.png',p,width = 6, height = 4, bg = 'transparent')

