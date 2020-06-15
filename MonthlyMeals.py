'''
Project: Monthly Meals
Title: Send Monthly Meals
Author: Jack Remmert
Date: 5/23/2020
'''
# import packages
import pandas as pd

# import helpers
from helpers.Meal_Plan_ import Meal_Plan_Helper
from helpers import Calendar_Plot as cd
from helpers.Gmail_API_ import Gmail_API_Helper

def main():
    # Read Data
    file = 'user_info'
    info = pd.read_csv('input/'+file+'.csv', delimiter = ',')
    
    file = 'user_preferences'
    preferences = pd.read_csv('input/'+file+'.csv', delimiter = ',')
    # Initalize Meal Plan Helper class
    mph = Meal_Plan_Helper()
    
    # Create Timeframe Preference
    preferences['dates'] = preferences.Weekends.apply(mph.weekend_selection)
    
    # Create Meals for Each User
    preferences['Meal_Ids'] = preferences.apply(mph.compile_meals, axis=1)
    preferences['last_months_meals'] = preferences.Meal_Ids
    
    # Create Calendar for Each User
    preferences['img'] = preferences[['user_id', 'dates','Meal_Ids']].apply(
                                        cd.gg_monthly_meals, axis=1)
    
    # Initalize Gmail API Helper
    gmail_api = Gmail_API_Helper()
    
    # Join Images for each User Info
    user_info = info.merge(preferences[['user_id', 'img']]
                ,on='user_id', how='left')
    # Create the Email
    user_info['message'] = user_info.apply(gmail_api.create_message, args=(True), axis=1)
    # Send Email
    user_info.message.apply(gmail_api.send_email, axis=1)
    
if (__name__ == "__main__"):
    main()  