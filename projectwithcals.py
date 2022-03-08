#retrieving a list of recipes containing the specific ingredient the user inputs

#Step 1: Log into Edamam
#Step 2: Enter Ingredient, Number of Caolries, Dietary Requirments, Time
#Step 3: Search for Receipes that meet the Requirements
#Step 4: Add Recipes to a CSV File

import requests
import csv

def search(ingredient):

    base_url = "https://api.edamam.com/api/recipes/v2"
    params = {
        "app_key": "02f125d327663e227138dc49ed0070b5",
        "app_id": "abef4209",
        "type": "public",
        "q": ingredient
    }
    res = requests.get(base_url, params=params)
    data = (res.status_code)

    #json function converts the data into a python dictionary
    response_data = res.json()

    #inside this key the values are in a list of dictionaries
    recipe = response_data['hits']

    #Dietary req check
    dietary = input("Do you have any dietary requirements or allergies? ")
    if dietary == 'yes':
        ask = input("What dietary requirements or allergies do you have?")
        check_list = ["vegan", "vegetarian", "pescatarian", "gluten", "nut"]
        if ask in check_list:
            pass
        else:
            print("Sorry the option entered isn't suitable. The available options include vegan, vegetarian, pescatarian, gluten, nut")
    elif dietary == 'no':
        pass
    else:
        print("The input entered is not applicable, please enter yes  or no")
        quit()


    #Dietary req list
    check = {'vegan': ['Vegan'], 'vegetarian': ['Vegetarian'], 'pescatarian': ['Pescatarian'], 'gluten': ['Gluten-Free'],
             'nut': ['Peanut-Free', 'Tree-Nut-Free']}

    #Maximum Calories and Total cooking/preparing time
    cal = float(input("Enter the maximum amount of calories required in the recipe: "))
    total_time = float(input("What are your time limits for preparing meals in minutes? "))


    #sorting the recipe list of dictionaries by calories
    #key parameter used to call a function and returns a key to use for sorting purposes
    new_recipe_list = sorted(recipe, key=lambda k: k['recipe']['calories'])

    headers = ["Recipe Name", "Calories (kcal)", "Cuisine Type", "Meal Type", "Total Cooking Time (minutes)"]

    #Adding the results into the csv file
    with open('Edamam.csv', 'w', newline='') as edamam:
        contents = csv.writer(edamam)

        #write the header
        contents.writerow(headers)

    #print out each recipe from the list of dictionaries
        for i in new_recipe_list:
            if i['recipe']['calories'] < cal and i['recipe']['totalTime'] <= total_time:
                if dietary == "yes":
                    dietary_reqs = check[ask] #get the list of the specific ask
                    healthlabels = i['recipe']['healthLabels'] #get the list of the healthlabels in the recipe
                    recipe_issues = set(healthlabels).intersection(set(dietary_reqs)) #crosschecking to see if elements are the same in the list

                    if len(recipe_issues) > 0:
                        print("You can have {}".format(i['recipe']['label']))
                        print()
                        try:
                            contents.writerow([i['recipe']['label'], round(i['recipe']['calories'], 2), i['recipe']['cuisineType'][0],
                                          i['recipe']['mealType'][0], i['recipe']['totalTime']])
                        except:
                            contents.writerow([i['recipe']['label'], round(i['recipe']['calories'], 2),
                                          i['recipe']['mealType'][0], i['recipe']['totalTime']])
                    else:
                        print("You cannot have {}".format(i['recipe']['label']))
                        print()
                else:
                    print("You can have {}".format(i['recipe']['label']))
                    contents.writerow([i['recipe']['label'], i['recipe']['calories'], i['recipe']['cuisineType'][0],
                                      i['recipe']['mealType'][0], i['recipe']['totalTime']])


ingredient = input("Enter an Ingredient you want the recipe to include: ")
search(ingredient)