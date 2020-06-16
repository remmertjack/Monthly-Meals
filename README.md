[![HitCount](http://hits.dwyl.com/remmertjack/Monthly-Meals.svg)](http://hits.dwyl.com/remmertjack/Monthly-Meals)
# Monthly-Meals
Welcome to Monthly Meals! This project was deisgned due to the difficulty of making a menu every week and even for the entire month. According to my mom, who this project was originally designed for, *"It is extremly hard to think of what people would like to eat for dinner in this family."* This I am sure all parents and adults must feel because thinking about what to eat is a daily task. Thankfully, you came to the right place because this does it for you. This repositoary is for all of my code that selects the meals, creates the visualization, and sends an email using Gmail oauth2 protocal. I have also included all of the meals that my mom uses and even some example user info for your own testing purposes. For any comments or questions or even if you would like to sign up for Monthly Meals, please email mealsmonthly@gmail.com and I can discuss more about it. *Currently we are not sending emails programmatically, everything else is working unless discussed below.*

## Objective
Create a calendar of meals for the month. And by "week" I mean Monday - Friday (Saturday and Sunday options are coming). At first this sounded simple. Here are the recipes, randomize them, and BAM good to go?! Well not really. In my family we would prefer not to eat Chicken two days in a row or Fish more than twice a week. Therefore, each Meal was classified as either Chicken, Fish, or Meat (Vegan and Vegetarian options are coming, I promise). Then we calculate the week's types of meals or the categories for each night based on those inputs, determine the meals, create the calendar and BAM, now we are good to go! 

## Meal Preferences
Not all of us eat the same thing. Currently I have classified people as either Omnivores, Vegans, Vegetarians, or Pescatarians. Secondly, some of us have food sensitivities such as Gluten, Diary, Nuts, or Shellfish (as of version 1.0, only Shellfish is a sensitivity accounted for, my mom needs to read the recipes and see how sensitive they are, I am not a great cook. You may get some meal ideas that go against your sensitivity, if so please email mealsmonthly@gmail.com.). Also, although some users will be sensitive to some items, sometimes a substitution can be made, such as a Gluten Free option. 

## Table of Contents
###### Folders
1. figs
2. helpers
3. input
4. output
###### Files
1. MonthlyMeals.py
2. quickstart.py

### Coding Notes and how it works
The detail for each of these files can be found in their respective directory, this is meant as a high level explaination for others to get a better understanding of how it works.
Built on 3 main data files found in input: user_preferences, user_info, and meals and 1 main file: MonthlyMeals. First we create a Timeframe Preference, does the user want meals on the weekends or not (As of v1.0 only Weekdays are inclluded)? Second we create the scheudle of meals based on a user's preferences with various helper functions (found in helpers). Third we create the Calendar image (also in helpers). Fourth we send the email using Gmail (and if you guess this file is in helpers, you would be correct too).
figs is where all of the Calendar images are stored and output is there for testing purposes. 

### The Future
What are the next steps you ask? Fantastic question which I have laid out the steps for below.
1. Include Vegan and Vegetarian meal options (if you have some, please send them to mealsmonthly@gmail.com)
2. Include the option for Weekend meals
3. Send the recipes for all of your meals in a pdf when the Calendar is sent
4. Create grocery lists based on when the user buys their groceries
5. Create a website where the user can input their various Diets and Sensitivites and view a menu such that the user can click on a meal and it displays the recipe. (Maybe in the Future Future)

###### Disclaimer
This project is not responsable for telling you what to eat. If you eat something on the menu that you are allergic to or do not like, that is not our responsibility. If you have a concern, please email mealsmonthly@gmail.com. 
