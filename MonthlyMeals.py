'''
Project: Monthly Meals
Title: Send Monthly Meals
Author: Jack Remmert
Date: 5/23/2020
'''
# working directory
import os
#path = r"/Users/Jack_Remmert/OneDrive/Portfolio/recipes"
path = r"C:\Users\remme\OneDrive\Portfolio\recipes"
os.chdir(path)

# import packages
import pandas as pd

# import helpers
#from helpers import Send_Email as se
from helpers import Calendar_Plot as cd
from helpers import Meal_Plan_Inputs as mpi
from helpers.fixer_functions import fix_Meal_Plan as ffmp
# user preferences
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)

'''
Read and Compile Data
'''
file = 'user_info'
info = pd.read_csv('input/'+file+'.csv', delimiter = ',')

file = 'user_preferences'
preferences = pd.read_csv('input/'+file+'.csv', delimiter = ',')

'''
Create Timeframe Preference
''' 
preferences['dates'] = preferences.Weekends.apply(mpi.weekend_selection)

'''
Create Meals for Each USer
''' 
user_meals = preferences.apply(schedule)

#==========
# Create Images for Each Diet
df = pd.read_csv('output/meals.csv')
df = df.loc[pd.notnull(df["Meals"])]
dates = df.dates
cats = df.Category
meals = df.Meals
p = cd.gg_monthly_meals(dates, meals, False)
#==========
# Send Emails
data.apply(se.send_email, args(user_email, user_firstname))
