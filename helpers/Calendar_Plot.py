'''
Project: Monthly Meals
Title: Calendar Plot Function
Author: Jack Remmert
Date: 5/23/2020
'''
import pandas as pd
import numpy as np
import re
from plotnine import *

# import helper functions

# user helper functions

# user defined functions

# user preferences

# read meals
file = 'meals'
meals = pd.read_csv('input/'+file+'.csv', delimiter = ',')

def gg_monthly_meals (user_meals, missing_dates = False, saving = False):

    # define the color palette
    fill_colors = {'Chicken': '#fcc438'
                   ,'Fish': '#33FFD8'
                   ,'Meat':'#F6B6FA'
                   ,'Vegan':'#c290f5'
                   ,'Vegetarian':'#3BE00A'
              }
    dates = pd.Series(user_meals.dates)
    meal_ids = pd.Series(user_meals.Meal_Ids)
    user_id = user_meals.user_id
    # organize in a dataframe
    data = pd.concat([dates, meal_ids], axis=1)
    data.columns = ['dates','Meal_Id']
    data['dates'] = pd.to_datetime(data.dates, format='%m/%d/%Y')
    data = data.merge(meals[['Meal_Id','formatted_Meal','Category']]
            ,on='Meal_Id', how='left')
    
    # Do we want Missing Dates?
    if (missing_dates == True):
        timeframe = pd.DataFrame(pd.date_range(min(data['dates'])
                    ,max(data['dates'])), columns = ['dates'])
    else:
        timeframe = pd.DataFrame(data.dates, columns = ['dates'])
        
    tf = pd.merge(timeframe,data, how='left',on = 'dates'
                  ,left_index=True, right_index=True)
    tf['dow'] = tf['dates'].apply(lambda x: x.dayofweek)
    tf['Day_Name'] = tf['dates'].apply(lambda x: x.strftime("%A"))
    tf['Day_Number'] = tf['dates'].apply(lambda x: x.day)
    tf['Week'] = tf['dates'].apply(lambda x: x.isocalendar()[1])
    tf['Month'] = tf['dates'].apply(lambda x: x.month)
    tf['Month_Name'] = tf['dates'].apply(lambda x: x.strftime('%B'))
    tf['Week_Month'] = tf.Week - min(tf.Week)
    tf['y'] = max(tf.Week_Month) - tf.Week_Month
    tf['Year'] = tf['dates'].apply(lambda x: x.year)  
    
    # Set up the title
    month = np.unique(tf.Month_Name)
    title = month[0] + " " + str(max(tf.Year))
    # fix missing categories
    tf['Category']=tf.Category.fillna('NAs')
    # fix missing meals
    tf['Meals']=tf.formatted_Meal.fillna('')
      
    # Get Current Day Names
    day_names_ = {
             0:'Monday', 1:'Tuesday',2:'Wednesday',3:'Thursday'
             ,4:'Friday',5:'Saturday', 6: 'Sunday' 
             }
  
    current_day_names = list(np.unique(tf.Day_Name))
    day_names = dict(filter(lambda elem: elem[1] in current_day_names, day_names_.items()))
    day_names = list(day_names.values())
    
    # Fix Meals with \n
    tf.Meals = tf.Meals.apply(lambda x: re.sub("\\\\n", "\n", x))
    
    # Define the x-axis as a row because plotnine does not allow position='top'
    # for axis. Thus create new geom_tile that visually operates as the row
    # Category == filler with Meal = Day
    # Set the y value to max(tf.y)+1; we want it aboe the first row.
    xaxis = pd.DataFrame.from_dict(day_names_, orient='index'
                                   ,columns = ['Day_Name'])
    xaxis['y'] = max(tf.y)+1
    xaxis['dow'] = xaxis.index 
    
    # fix color scheme based on user categories
    cats = list(np.unique(tf.Category))
    clrs = {category: clr for category, clr in fill_colors.items() if category in cats}
    
    p = ggplot() +\
            geom_tile(aes(x='dow', y='y', fill = 'Category'), tf.loc[tf.Category != 'NAs'], color='black') +\
            geom_tile(aes(x='dow', y='y'), tf.loc[tf.Category == 'NAs'], color='black', fill = '#FFFFFF') +\
            geom_tile(aes(x='dow', y='y'), xaxis[xaxis.Day_Name.isin(day_names)], color='black', fill = '#fff8dc') +\
            geom_text(aes(x='dow', y='y', label = tf.Meals), tf, size=7.25) +\
            geom_text(aes(x='dow', y = tf.y+.4, label = 'Day_Number'), tf, size=8) +\
            geom_text(aes(x='dow', y = 'y', label = 'Day_Name'), xaxis[xaxis.Day_Name.isin(day_names)], size=10) +\
            scale_y_continuous(expand=(0,0)) +\
            scale_fill_manual(breaks = np.array(list(clrs.keys())), values = np.array(list(clrs.values()))) + \
            scale_size_identity()+\
            ggtitle(title)+\
            theme(
              panel_background = element_rect(fill='white')
              ,legend_title = element_blank()
              ,legend_text = element_text(size = 10)
              ,axis_ticks=element_blank()
              ,axis_title=element_blank()
              ,axis_text_y = element_blank()
              ,axis_text_x = element_blank()
              ,legend_position = 'bottom'
              )
    image_name = 'figs/calendar_' + str(user_id) + '_.png'
    if saving == True:
        p.save(filename = image_name, width = 11, height = 6.8, bg = 'transparent', verbose=False) 
    return p

'''
Useful ggplot but not used:
    scale_x_continuous(expand=(0,0), breaks=x_breaks, labels=day_names)
'''