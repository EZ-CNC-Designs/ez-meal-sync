import time, json, os
from pathlib import Path
from dotenv import load_dotenv
import pyinputplus as pyip
import gkeepapi
from gkeep.gkeep_gen_mastertoken import mastertoken_generator
from gkeep.gkeep_actions import GKeepActions


class UserInterface:
    """Allow the user to modify meals and ingredients and update program settings."""   
    def __init__(self, user_name):
        # Define file paths
        self.GROCERY_FILE_PATH = "data/grocery.json"
        self.MEALS_FILE_PATH = "data/meals.json"
        

        # self.USER_GROCERY_STORE_TITLE = user_grocery_store + " List"
        self.CURRENT_MEALS_NOTE_NAME = "Current Meals"
        self.NEXT_MEALS_NOTE_NAME = "Upcoming Meals"

        # Load grocery and meal data
        self.grocery_items = self._load_json(self.GROCERY_FILE_PATH)
        self.meals_items = self._load_json(self.MEALS_FILE_PATH)
        self.user_name = user_name

        load_dotenv()
        # Retrieve the email address
        os.getenv("GKEEP_EMAIL")

        self.MASTER_TOKEN_PATH = Path('settings/master_token.txt')
        # Retrieve the master token
        os.getenv("GKEEP_MASTERTOKEN")

        self.email_address = "placeholder"
        self.mstr_tkn = "placeholder"
        

        # if self.email_address and self.mstr_tkn:
        #     self.keep = gkeepapi.Keep()
        #     self.keep.authenticate(self.email_address, self.mstr_tkn)

    def _load_json(self, file_path):
        """Helper method to load JSON data from a file."""
        with open(file_path, 'r') as file:
            return json.load(file)

    def _save_json(self, data, file_path):
        """Helper method to save data to a JSON file."""
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def main_menu(self):
        """Main menu options."""
        run_main_menu = True
        while run_main_menu == True:
            menu_opt = pyip.inputNum(f"""\nWelcome to EZ Meal Sync's User Interface, {self.user_name}!
    Enter a number (followed by enter) to do the following:
    1 = Create a new meal option
    2 = Modify/delete a meal option
    3 = Modify/delete an ingredient
    4 = Modify next week meals list
    5 = Modify settings
    6 = Return to the main menu\n\n""", max=6)

            if menu_opt == 1:
                self.create_meal()
            elif menu_opt == 2:
                self.mod_meal_option()
            elif menu_opt == 3:
                self.mod_ingredients()
            elif menu_opt == 4:
                self.mod_next_meals()
            elif menu_opt == 5:
                self.mod_settings()
            elif menu_opt == 6:
                run_main_menu = False

    def create_meal(self):
        """Add a meal with corresponding ingredients into a JSON dictionary."""
        run_create_meal = True
        while run_create_meal == True:
            meal_name = pyip.inputStr('\nEnter a meal name or enter "Quit" to return to the main menu.\n\n')
            fixed_meal_name = meal_name.title()

            # Return to the main menu.
            if fixed_meal_name == "Quit":
                run_create_meal = False
            # Check if meal has already been created.
            elif fixed_meal_name in self.meals_items:
                print(f'{fixed_meal_name} has already been created. Choose a different meal or enter "Quit" to return to the main menu.')
                continue
            else:
                verify_meal_name = pyip.inputYesNo(f"\nYou entered {fixed_meal_name}. Is this correct? (Yes/No)\n\n")
                if verify_meal_name == "yes":
                    # Add ingredients for the new meal.
                    while True:
                        ingredient_list = input(f'\nEnter a list of ingredients, separated by commas for the meal "{fixed_meal_name}".\n\n')
                        split_ingredient_list = ingredient_list.split(",")
                        fixed_ingredient_list = [ingredient.title().strip() for ingredient in split_ingredient_list]
                        
                        verify_ingredients = pyip.inputYesNo(f"\nYou entered the following ingredients. Are they correct (yes or no)?\n{fixed_ingredient_list}\n\n")
                        if verify_ingredients == "yes":
                            print(f"\n{fixed_meal_name} was added to the dictionary with the following ingredients:\n{fixed_ingredient_list}\n\n")
                            # Add meal name and ingredients to the dictionary.
                            existing_data = self._load_json(self.MEALS_FILE_PATH)
                            existing_data[fixed_meal_name] = fixed_ingredient_list
                            self._save_json(existing_data, self.MEALS_FILE_PATH)
                            time.sleep(2)

                            # Check if ingredients are categorized.
                            for item in fixed_ingredient_list:
                                found = False
                                for supply in self.grocery_items.values():
                                    if item in supply:
                                        found = True
                                        break
                                if not found:
                                    print(f"\n{item} is not categorized.")
                                    # Open the grocery.json file and update it.
                                    existing_data = self._load_json(self.GROCERY_FILE_PATH)
                                    categories = list(existing_data.keys())
                                    select_category = pyip.inputChoice(prompt=f"Select a category for {item}:\n{categories}\n\n", choices=categories)

                                    existing_data[select_category].append(item)
                                    self._save_json(existing_data, self.GROCERY_FILE_PATH)
                        elif verify_ingredients == "no":
                            continue
                elif verify_meal_name == "no":
                    continue

    def mod_meal_option(self):
        """Delete or modify a created meal option."""
        
        note_choices = ["Next Week Meals", "Current Week Meals"]
        note_to_get = pyip.inputChoice(note_choices, blank=True)
        note_content = GKeepActions(user_email=self.email_address,
                                    user_master_token=self.mstr_tkn,
                                    user_grocery_store=None,
                                    current_meal_note_name=self.CURRENT_MEALS_NOTE_NAME,
                                    next_meal_note_name=self.NEXT_MEALS_NOTE_NAME
                                    ).pull_note_content(note_to_get)
        for content in note_content:
            print(content)

        pyip.inputChoice(note_content,)
        # Display all the meal options
        # Select a meal to delete or modify
        # If delete, remove the ingredients while checking for usage by other meals
        # If modify, add the ingredients or remove the ingredients while checking for usage by other meals

    def mod_ingredients(self):
        """Delete or modify an ingredient."""
        pass
        # Display all the ingredients
        # Select which ingredient to modify or delete
        # If the ingredient is used in a 


    def mod_next_meals(self):
        """Make a change to the created meal list."""
        pass
        # Choose next week or current meals
        # Display the meals
        # Choose which meal you want to remove
        # Replace the empty slot with a random meal
        # Regenerate the ingredient list

    def mod_settings(self):
        """Adjust users settings."""
        run_settings = True
        while run_settings == True:
            prompt = pyip.inputInt(f"""\nEnter a number to do the following:
    1 = Configure your email address
    2 = Define your master token
    3 = Configure your grocery store
    4 = Assign the number of meals to be generated
    5 = Return to the main menu\n\n""", max=5)
            if prompt == 1:
                # Configure the users email address
                if self.email_address:
                    print(f"\nYour current email is listed as: {self.email_address}")
                    time.sleep(2)
                address = pyip.inputEmail("\nEnter an email address or leave blank to return to your setting options.\n\n", blank=True)
                if address:
                    self.email_path.write_text(address)
                    self.email_address = address
                    print(f"\nYour email has been updated to {self.email_address}.")
                    
            elif prompt == 2:
                # Receive a master token
                if self.email_address:
                    oauth_token = pyip.inputStr("""\nEnter your oauth token to generate a master token or leave blank to return to the settings options.\n\n""",
                                                blank=True)
                    if oauth_token:
                        print("Generating a master token.")
                        mstr_token = mastertoken_generator(self.email_address, oauth_token)
                        if mstr_token:
                            master_token_path = Path('settings/master_token.txt')
                            master_token_path.write_text(mstr_token)
                           
                            print("Your master token has been successfully generated and stored.")
                            print("Do not share your master token with anyone as it can be used to access your Google Keep.")
                            time.sleep(2)
                    else:
                        continue
                else:
                    print("You have not yet entered your email address.")        
                    print("Go to the settings and enter one now.")
                    time.sleep(2)           

            elif prompt == 3:
                # Configure your grocery store
                path = Path("settings/grocery_store.txt")
                contents = path.read_text()
                if contents:
                    print(f"\nYour current grocery store is listed as: {contents}.")
                    time.sleep(2)
                store_options = ["Aldi", "Festival Foods", "Trader Joe's", "Pick N' Save", "Piggly Wiggly", "Woodman's"]
                store_selection = pyip.inputChoice(choices=store_options, blank=True,
                                                   prompt=f"""\nEnter a store from the following list or leave blank to return to the settings options.
        {store_options}\n\n""")
                if store_selection:
                    path.write_text(store_selection)
                    print(f"\nYour store has been updated to {store_selection}.")
            
            elif prompt == 4:
                # Assign the number of meals to be generated
                path = Path("settings/num_meals.txt")
                contents = path.read_text() 
                if contents:
                    print(f"\nYour current number of meals is set at: {contents}")
                    time.sleep(2)
                num_meals = pyip.inputNum("\nEnter how many meals you want to be generated when the program is ran or leave blank to return to the settings options.\n\n",
                                          blank=True)
                if num_meals:
                    path.write_text(str(num_meals))
                    print(f"\n{num_meals} will be generated when your program is ran.")

            elif prompt == 5:
                # Exit the settings menu
                run_settings = False
