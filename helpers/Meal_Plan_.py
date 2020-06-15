'''
Project: Monthly Meals
Title: Meal Plan Helper
Author: Jack Remmert
Date: 5/1/2020
'''
# import packages
import pandas as pd
import random
from numpy.random import choice
from datetime import date, datetime
import calendar
from collections import OrderedDict

# import helpers
from helpers.fixer_functions import fix_Meal_Plan as ffmp

# user preferences
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 40)

class Meal_Plan_Helper(object):
    meals = None
    data = None
    meat = None
    chicken = None
    fish = None
    vegan = None
    veggie = None
    #logging_config_filepath = ""
    #logging.config.fileConfig(logging_config_filepath)
    
    def __init__(self):
        # read meals
        file = 'meals'
        self.meals = pd.read_csv('input/'+file+'.csv', delimiter = ',')
        
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
        self.data = data.loc[(data.Weekday <5)]
        # create meals per each category
        self.meat = list(self.meals.Meal_Id.loc[self.meals.Category == 'Meat'])
        self.chicken = list(self.meals.Meal_Id.loc[self.meals.Category == 'Chicken'])
        self.fish = list(self.meals.Meal_Id.loc[self.meals.Category == 'Fish'])
        self.vegan = list(self.meals.Meal_Id.loc[self.meals.Category == 'Vegan'])
        self.veggie = list(self.meals.Meal_Id.loc[self.meals.Category == 'Vegetarian'])
        
        # Create Diet DataFrames
        self.omni_diet = self.meals.Meal_Id.loc[self.meals.Omnivore == 1]
        self.pescat_diet = self.meals.Meal_Id.loc[self.meals.Pescatarian == 1]
        self.vegan_diet = self.meals.Meal_Id.loc[self.meals.Vegan == 1]
        self.veggie_diet = self.meals.Meal_Id.loc[self.meals.Vegetarian == 1]
    
    # Are we doing Weekdays or Weekends or Both?
    def weekend_selection(self, weekend):
        # if weekends is 0 as in not want weekends, then return M-F or 0-4
        if weekend == False:
            return list(self.data.dates.loc[(self.data.Weekday <5)])
        else:
            return list(self.data.dates)
    # Which Meals are applicable for the diet?
    def meal_filter_from_diet(self, diet):
        if diet == 'Vegan':
            diet_data = self.vegan_diet
        elif diet == 'Vegetarian':
            diet_data = self.veggie_diet
        elif diet == 'Pescatarian':
            diet_data = self.pescat_diet
        else:
            diet_data = self.omni_diet
        return list(diet_data)
    
    # Which Meals are applicable for the sensitivity?
    def meal_filter_from_sens(self, gf, df, nf, sff, meal_ids):
        sens_data = self.meals
        if gf == 1:
            sens_data = sens_data.loc[sens_data.GF_Option == 1]
        if df == 1:
            sens_data = sens_data.loc[sens_data.Diary_Free == 1]
        if nf == 1:
            sens_data = sens_data.loc[sens_data.Nut_Free == 1]
        if sff == 1:
            sens_data = sens_data.loc[sens_data.Shellfish_Free == 1]
        
        return list(set(meal_ids) & set(sens_data.Meal_Id))
        
        #return list(sens_data)
    # Which Meals?
    def meal_id_list(self, prefs, diet):
        # filter on diet
        meal_ids_fromDiet = self.meal_filter_from_diet(diet)
        # filter on sensitivity
        meal_ids_fromSens = self.meal_filter_from_sens(prefs.Gluten_Free, prefs.Diary_Free
                                         ,prefs.Nut_Free, prefs.Shellfish_Free,
                                         meal_ids_fromDiet)
        return meal_ids_fromSens
    
    def cats_per_week(self, prefs):
        # What Categories of Food would the user like?
        li_cats = list(OrderedDict.fromkeys(self.meals.Category))
        weight_cats = list([prefs.nChicken, prefs.nFish, prefs.nMeat,
                           prefs.nVegan, prefs.nVegetarian])
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
        li_cats = list(OrderedDict.fromkeys(self.meals.Category))
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
        if pd.Series(main).value_counts().max()>5:
            return main
        else:
            li = ffmp.fx_cats(main)
            return li
        
    def compile_meals(self, prefs, testing = False):
        # What Meals would the User like?
        meal_ids_ = self.meal_id_list(prefs, prefs.Diet)
        # filter on last months meals
        
        
        data = pd.DataFrame(prefs.dates, columns = ['dates'])
        data['Week'] = data['dates'].apply(lambda x: x.isocalendar()[1])
        data['Week_Month'] = data.Week - min(data.Week)
        
        cats = []
        for week in data.groupby('Week_Month'):
            li = []
            li = self.cats_per_week(prefs)
            # Append Category list onto the data
            days = len(week[1])
            li = li[:days]
            cats.extend(li)
        
        data['Category'] = cats
        # Sort by Category
        # Will always be Chicken, Fish, Meat, Vegan, Vegetarian after sorting
        data = data.sort_values(by=['Category','dates'])
        # How many Meals of each category?
        chi_n = len(data.loc[data.Category == 'Chicken'])
        fish_n = len(data.loc[data.Category == 'Fish'])
        meat_n = len(data.loc[data.Category == 'Meat'])
        vegan_n = len(data.loc[data.Category == 'Vegan'])
        veggie_n = len(data.loc[data.Category == 'Vegetarian'])
        # filter on meals the user can eat
        chicken = [x for x in self.chicken if x in meal_ids_]
        fish = [x for x in self.fish if x in meal_ids_]
        meat = [x for x in self.meat if x in meal_ids_]
        vegan = [x for x in self.vegan if x in meal_ids_]
        veggie = [x for x in self.veggie if x in meal_ids_]
        # random.choice with n to get those lists
        # if not enough options, then sample with replacement
        try: chick_meals = list(choice(chicken, chi_n, False))
        except: chick_meals = list(choice(chicken, chi_n, True))
        try: fish_meals = list(choice(fish, fish_n, False))
        except: fish_meals = list(choice(fish, fish_n, True))
        try: meat_meals = list(choice(meat, meat_n, False))
        except: meat_meals = list(choice(meat, meat_n, True))
        try: vegan_meals = list(choice(vegan, vegan_n, False))
        except: vegan_meals = list(choice(vegan, vegan_n, True))
        try: veggie_meals = list(choice(veggie, veggie_n, False))
        except: veggie_meals = list(choice(veggie, veggie_n, True))
        # combine all together
        meal_ids = chick_meals + fish_meals + meat_meals + vegan_meals + veggie_meals
        # Append Meal Ids to Data
        data['Meal_Id'] = meal_ids
        # Append Meals
        meal_data = pd.merge(data, self.meals[['Meal_Id','formatted_Meal']], on = 'Meal_Id')
        # Sort by Date
        meal_data = meal_data.sort_values(by='dates')
        if testing == False:
            meal_data = meal_data.drop(['formatted_Meal'],axis=1)
        
        return list(meal_data.Meal_Id)
              
