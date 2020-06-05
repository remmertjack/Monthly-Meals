'''
Project: Monthly Meals
Title: compile recipes
Author: Jack Remmert
Date: 5/1/2020
'''
# import packages
import pandas as pd
import random
from numpy.random import choice
from datetime import date, datetime
import calendar
from collections import OrderedDict, Counter

# import helpers
from helpers.fixer_functions import fix_Meal_Plan as ffmp

# user preferences
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 40)
  
# read meals
file = 'meals'
meals = pd.read_csv('input/'+file+'.csv', delimiter = ',')

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
data = data.loc[(data.Weekday <5)]


# Are we doing Weekdays or Weekends or Both?
def weekend_selection(weekend):
    # if weekends is 0 as in not want weekends, then return M-F or 0-4
    if weekend == False:
        return list(data.dates.loc[(data.Weekday <5)])
    else:
        return list(data.dates)
# Which Meals are applicable for the diet?
def meal_filter_from_diet(diet):
    if diet == 'Vegan':
        diet_data = meals.Meal_Id.loc[meals.Vegan == 1]
    elif diet == 'Vegetarian':
        diet_data = meals.Meal_Id.loc[meals.Vegetarian == 1]
    elif diet == 'Pescatarian':
        diet_data = meals.Meal_Id.loc[meals.Pescatarian == 1]
    else:
        diet_data = meals.Meal_Id
    return list(diet_data)

# Which Meals are applicable for the sensitivity?
def meal_filter_from_sens(gf, df, nf, sff, meal_ids):
    sens_data = meals
    if gf == 1:
        sens_data = sens_data.loc[sens_data.GF_Option == 1]
    if df == 1:
        sens_data = sens_data.loc[sens_data.Diary_Free == 1]
    if nf == 1:
        sens_data = sens_data.loc[sens_data.Nut_Free == 1]
    if sff == 1:
        sens_data = sens_data.loc[sens_data.Shellfish_Free == 1]
    
    return list(set(meal_ids) & set(sens_data.Meal_Id))
    
    return list(sens_data)
# Which Meals?
def meal_list(prefs):
    # filter on diet
    meal_ids_ = meal_filter_from_diet(prefs.Diet)
    # filter on sensitivity
    meal_ids = meal_filter_from_sens(prefs.Gluten_Free, prefs.Diary_Free
                                     ,prefs.Nut_Free, prefs.Shellfish_Free,
                                     meal_ids_)
    return meal_ids

def cats_per_week(prefs):
    # What Categories of Food would the user like?
    li_cats = list(OrderedDict.fromkeys(meals.Category))
    weight_cats = list([prefs.nChicken, prefs.nFish, prefs.nMeat,
                       prefs.nVegan, prefs.Vegetarian])
    # Check if desired options exceed number of possible days
    if prefs.Weekends == 0 and sum(weight_cats)>5:
        print("Weight Category Error for user: " + str(prefs.user_id))
        exit()
    if prefs.Weekends == 1 and sum(weight_cats)>7:
        print("Weight Category Error for user: " + str(prefs.user_id))
        exit()
    main = []  
    for li_cats, weight_cats in zip(li_cats, weight_cats):
        main.extend([li_cats] * weight_cats)
    
    # Select which Category for the final day(s)
    li_cats = list(OrderedDict.fromkeys(meals.Category))
    op_cats = list([prefs.OP_Chicken, prefs.OP_Fish, prefs.OP_Meat,
                       prefs.OP_Vegan, prefs.OP_Vegetarian])
    pos_cats = []  
    for li_cats, op_cats in zip(li_cats, op_cats):
        pos_cats.extend([li_cats] * op_cats)
    if len(main) < 5:
        while(len(main)!=5):
            x = random.choice(pos_cats)
            main.append(x)
    random.shuffle(main)
    #max(Counter(main))
    li = ffmp.fx_cats(main)
    return li
    
def schedule(prefs):
    # What Meals would the User like?
    prefs.meal_ids = meal_list(prefs)
    
    
    data = pd.DataFrame(prefs.dates, columns = ['dates'])
    data['Week'] = data['dates'].apply(lambda x: x.isocalendar()[1])
    data['Week_Month'] = data.Week - min(data.Week)
    
    for week in data.groupby('Week_Month'):
        li = []
        li = cats_per_week(prefs)
        # Append Category list onto the data
        days = len(week[1])
        li = li[:days]
        cats.extend(li)
    
    
    
'''
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
data = data.drop(['WeekNo'],axis=1)

data['Category'] = data.Category.apply(lambda x: 'Off' if isinstance(x, float) else x)
data['Meals'] = data.Meals.apply(lambda x: '' if isinstance(x, float) else x)

# Write to CSV
data.to_csv('output/meals.csv', index = False)

def meal_selection(diet = 'Omniovore'):
    pass
#    if diet == 'Vegan':
#        meals = vegan_meals()
#    elif diet == 'Vegetarian':
#        meals = veggie_meals()
#    elif diet == 'Pescatarian':
#        meals = pescat_meals()
#    else:
#        meals = omni_meals()
#    return meals

'''


            
