'''
Project: Monthly Meals
Title: compile recipes
Author: Jack Remmert
Date: 5/1/2020
'''
# working directory
import os
path = r"/Users/Jack_Remmert/OneDrive/Portfolio/recipes"
#path = r"C:\Users\remme\OneDrive\Portfolio\recipes"
os.chdir(path)

# import packages
import pandas as pd
import random
from numpy.random import choice
from datetime import date, datetime
import calendar

# import helpers
from helpers.fixer_functions import fix_Meal_Plan as ffmp

# user preferences
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 40)
  
# read meals
file = 'meals'
df = pd.read_csv('input/'+file+'.csv', delimiter = ',')

# Define the Categories
meat = list(df.formatted_Meal.loc[df.Category == 'Meat'])
chicken = list(df.formatted_Meal.loc[df.Category == 'Chicken'])
fish = list(df.formatted_Meal.loc[df.Category == 'Fish'])
vegan = list(df.formatted_Meal.loc[df.Category == 'Vegan'])
veggie = list(df.formatted_Meal.loc[df.Category == 'Vegetarian'])

# define the month
tdy = date.today()
nxt_month = calendar.nextmonth(tdy.year,tdy.month)[1]
yr = calendar.nextmonth(tdy.year,tdy.month)[0]
last_day_of_month = calendar.monthrange(yr,nxt_month)[1]
# fix month into proper format
nxt_month = ffmp.fx_month(nxt_month)
start_date = str(yr) +'-'+str(nxt_month)+'-0'+ str(1)
end_date = str(yr) +'-'+str(nxt_month)+'-'+ str(last_day_of_month)
start_date=datetime.strptime(start_date,'%Y-%m-%d')
end_date=datetime.strptime(end_date,'%Y-%m-%d')
# create date range
data = pd.DataFrame(pd.date_range(start_date,end_date))
data.columns = ['dates']
data['Weekday']=data.dates.dt.dayofweek
data['Week']=data['dates'].apply(lambda x: x.isocalendar()[1])
data['Week_Month'] = data.Week - min(data.Week)
data = data.loc[(data.Weekday <5)]
data = data.drop(['Week'],axis=1)
 
# Append Category
cats = []
for week in data.groupby('Week_Month'):
    # Which Category of Food
    # Options are Chicken, Meat, or Fish
    main = ['Chicken', 'Fish', 'Meat', 'Fish']
    # Select which Category for the final 5th day
    x = random.random()
    if x < 0.4:
        last = 'Chicken'
    else:
        last = 'Meat'
    main.append(last)
    # Shuffle and Fixe Categories
    random.shuffle(main)
    li = ffmp.fx_cats(main)
    # Append Category list onto the data
    days = len(week[1])
    li = li[:days]
    cats.extend(li)

# Append Category to Data
data['Category'] = cats
# Sort by Category
# Will always be Chicken, Fish, then Meat after sorting
data = data.sort_values(by=['Category','dates'])
# How many Meat, Fish, and Chicken Meals?
chi_n = len(data.loc[data.Category == 'Chicken'])
fish_n = len(data.loc[data.Category == 'Fish'])
meat_n = len(data.loc[data.Category == 'Meat'])
# random.choice with n to get those lists
chick_meals = list(choice(chicken, chi_n, False))
fish_meals = list(choice(fish, fish_n, False))
meat_meals = list(choice(meat, meat_n, False))
meals = chick_meals + fish_meals + meat_meals
# Append Meals to Data
data['Meals'] = meals
# Sort by Date
data = data.sort_values(by='dates')

# Data Manipulation to help with Plotting
# create date range
dates = pd.DataFrame(pd.date_range(start_date,end_date))
dates.columns = ['dates']
data = dates.merge(data, on = 'dates',how = 'left')
data['Weekday']=data.dates.dt.dayofweek
data = data.drop(['Week_Month','Weekday'],axis=1)

data['Category'] = data.Category.apply(lambda x: 'Off' if isinstance(x, float) else x)
data['Meals'] = data.Meals.apply(lambda x: '' if isinstance(x, float) else x)

# Write to CSV
data.to_csv('output/meals.csv', index = False)



            
