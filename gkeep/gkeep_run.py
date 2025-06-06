import sys, json, webbrowser, time, os
from pathlib import Path
import gkeepapi
from gkeep.gkeep_actions import GKeepActions
from gkeep.gkeep_manip_meals import generate_new_meals

def run_meal_planning():
    # Open the Google Keep website.
    # webbrowser.open("keep.google.com")

    # Paths to user info.
    email_path = Path("settings/user_email.txt")
    user_email = email_path.read_text()
    master_token_path = Path("settings/master_token.txt")
    user_master_token = master_token_path.read_text()

    # Import the grocery store name.
    grocery_store_path = Path("settings/grocery_store.txt")
    user_grocery_store = grocery_store_path.read_text()

    # Set list names.
    USER_GROCERY_STORE_TITLE = user_grocery_store + " List"
    CURRENT_MEALS_NOTE_NAME = "Current Meals"
    NEXT_MEALS_NOTE_NAME = "Upcoming Meals"

    # 3 standard note names combined into a list.
    standard_note_names = [USER_GROCERY_STORE_TITLE,
                           CURRENT_MEALS_NOTE_NAME,
                           NEXT_MEALS_NOTE_NAME]
    
    # Load the grocery store department names.
    grocery_dept_path = "data/grocery.json"
    with open(grocery_dept_path, "r") as grocery_file:
        grocery_dict = json.load(grocery_file)

    departments = []
    for department in grocery_dict.keys():
        departments.append(department)
    
    # Make an instance of the GKeepActions class.
    gkact = GKeepActions(user_email=user_email,
                         user_master_token=user_master_token,
                         user_grocery_store=USER_GROCERY_STORE_TITLE,
                         current_meal_note_name=CURRENT_MEALS_NOTE_NAME,
                         next_meal_note_name=NEXT_MEALS_NOTE_NAME)

    # Verify the notes are created, if not create it.
    gkact.create_gnote(note_names=standard_note_names)

    # Delete any checked items within the grocery store list only.
    gkact.delete_checked(USER_GROCERY_STORE_TITLE)

    # Pull list data to later be manipulated.
    exist_grocery_content = gkact.pull_note_content(USER_GROCERY_STORE_TITLE)
    exist_current_meals_content = gkact.pull_note_content(CURRENT_MEALS_NOTE_NAME)
    exist_upcoming_meals_content = gkact.pull_note_content(NEXT_MEALS_NOTE_NAME)

    # Load the meals list.
    meals_path = "data/meals.json"
    with open(meals_path, "r") as meals_file:
        all_meals = json.load(meals_file)

    # List of all meal names in the dict.
    user_meal_names = []
    for meal_name in all_meals.keys():
        user_meal_names.append(meal_name)

    # Path to number of meals to be generated.
    num_meals_path = Path("settings/num_meals.txt")
    user_num_meals = num_meals_path.read_text()

    # Generate a list of meals.
    new_meals = generate_new_meals(all_meals=user_meal_names,
                                   current_meals=exist_current_meals_content,
                                   upcoming_meals=exist_upcoming_meals_content,
                                   meal_qty=user_num_meals)
    
    # Delete the contents in Current and Upcoming meals.
    gkact.delete_contents(NEXT_MEALS_NOTE_NAME)
    gkact.delete_contents(CURRENT_MEALS_NOTE_NAME)
    
    # Move contents from Upcoming meals to Current.
    # Add new meals to Upcoming.
    gkact.add_contents(NEXT_MEALS_NOTE_NAME, new_meals)
    gkact.add_contents(CURRENT_MEALS_NOTE_NAME, exist_upcoming_meals_content)

    # Generate a list of ingredients based off of the new meals list.
    # Retrieve the old grocery list.
    # Delete any checked items.
    # Any unchecked items that are not department names will be added to the new list.
    # Ensure the list is properly organized and indented.
    # Add the new list back into Google Keep.



    print("The EZ Meal Sync program was successful! Google Keep has been updated with the latest content.")
    os._exit(0)