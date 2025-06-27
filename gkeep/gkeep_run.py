import os, tkinter as tk, time, json, random
from tkinter import ttk
from tkinter import messagebox
import gkeepapi, gpsoauth, dotenv, soundplay
from gkeepapi.exception import LoginException
from typing import Optional


class GKeepGenMastToken:
    """Generate a master token to be used for Google Keep's API."""
    def __init__(self):
        pass


    def mastertoken_generator(self, email: str, oauth_token: str, android_id='0123456789abcdef')-> Optional[str]:
        """Generates a master token to be used for Google Keep's API.
        Takes the users email address and an oauth token and returns a master token or None."""
    
        # Android ID is generic id as it is irrelevant
        # Exchange the OAuth token for a master token
        master_response = gpsoauth.exchange_token(email, oauth_token, android_id)

        if 'Token' in master_response:
            master_token = master_response['Token']
            return master_token
        else:
            return None
        

class GKeepActions(gkeepapi.Keep):
    def __init__(self):
        """Connect to Google Keep and manipulate notes."""
        super().__init__() # Inherit gkeepapi
        
        # Login credentials
        self.email = os.getenv('GKEEP_EMAIL')
        self.master_token = os.getenv('GKEEP_MASTERTOKEN')

        self.GROCERY_DEPTS = ['Produce', 'Bakery', 'Deli', 'Meat', 'Dairy', 'Frozen',
                            'Health', 'Cleaning Supplies']

        grocery_store_file = open('data/grocery_store.txt', 'r')
        self.grocery_store_name = grocery_store_file.read()
        # Set list names
        self.GROCERY_STORE_LIST = str(self.grocery_store_name) + " List"
        self.CURRENT_MEALS_LIST = "Current Meals"
        self.UPCOMING_MEALS_LIST = "Upcoming Meals"
        self.ALL_LIST_NAMES = [self.GROCERY_STORE_LIST, self.CURRENT_MEALS_LIST, self.UPCOMING_MEALS_LIST]


    def current_progress(self):
        """Show the current progress of meal generation."""
        self.progress_window = tk.Tk()
        self.progress_window.title('EZ Meal Sync Progress')
        self.progress_window.geometry('500x500')

        self.progress_message = tk.Label(master=self.progress_window, text='Starting EZ Meal Sync')
        self.progress_message.pack()

        self.progress_bar = ttk.Progressbar(master=self.progress_window)
        self.progress_bar.pack()

        # self.progress_message.update()
        # time.sleep(.2)
        

    def verify_data(self):
        """Runs the meal sync program."""
        verify_run = messagebox.askyesno(title='Run Meal Sync?', message='Are you sure that you want to run Meal Sync?\nThis action cannot be undone.')
        if verify_run == True:
            
            # Verify that an integer is set for the number of meals
            with open('data/meal_qty.txt') as file:
                self.num_meals = file.read()
                if self.num_meals.isdigit():
                    self.num_meals = int(self.num_meals)
                    file.close()
                else:
                    messagebox.showerror(title='Incorrect Number of Meals',
                                        message='Enter an integer for the number of meals.'
                                        f' Number of Meals to be generated is currently set to: {self.num_meals}')
                    return False
    
            # Verify that a master token exists
            verify_token = os.getenv('GKEEP_MASTERTOKEN')
            if not verify_token:
                messagebox.showerror(title='No Master Token',
                                    message='You have not yet generated a master token.')
                return False
            
            # Verify that an email exists
            verify_email = os.getenv('GKEEP_EMAIL')
            if not verify_email:
                messagebox.showerror(title='No Email Address',
                                    message='You have not yet entered an email address.')
                return False
            
            # Verify that a grocery store exists
            grocery_store_file = open('data/grocery_store.txt', 'r')
            verify_grocery_store = grocery_store_file.read()
            if not verify_grocery_store:
                messagebox.showerror(title='No Grocery Store Found',
                                    message='You have not yet entered a grocery store.')
                return False
            
            # self.current_progress() # Open the progress window if all contents are met
            

    def user_login(self):
        """Connect to the users Google Keep."""
        try:
            self.authenticate(email=self.email, master_token=self.master_token)
        except ConnectionError:
            messagebox.showerror(title='Connection Failed',
                                 message='Connection failed. Check your internet connection')
            return None

        except LoginException:
            messagebox.showerror(title='Failed Login',
                                 message='Your login failed. Regenerate a new master token & check your email address.')
            return None

    def create_lists(self):
        """Create the needed notes if they dont' exist."""
        # Move existing notes from trash or archive to the main menu
        all_notes = self.all() # Retrieve all notes on Google Keep
        already_created_notes = [] # Keep track of what notes have been created
        for note in all_notes:
            if note.title.strip() in self.ALL_LIST_NAMES:              
                note.archived = False # Unarchive
                note.untrash() # Untrash
                already_created_notes.append(note.title) # Add to already created
        # Create new notes if they don't already exist
        for note_name in self.ALL_LIST_NAMES:
            if note_name not in already_created_notes:
                self.new_list = self.createList(title=note_name) # Create a new note
                # self.progress_message.config(text=f'Creating note {note_name}')
                # self.progress_message.update()
                # time.sleep(.2)

        self.sync() # Save changes
           

    def adjust_grocery_list(self):
        """Set the grocery list with the correct categories."""

        gkeep_grocery_lists = list(self.find(query=self.GROCERY_STORE_LIST)) # Find the grocery list
        gkeep_grocery_list = gkeep_grocery_lists[0] # Use the first result
        self.old_grocery_list = [] # Make the old grocery list global
        for item in gkeep_grocery_list.items:
            self.old_grocery_list.append(item.text) # Pull contents and add to old grocery list
    
        # Add missing categories
        # TODO rearange categories so they are in the correct order
        for category in self.GROCERY_DEPTS:
            if category not in self.old_grocery_list:
                self.old_grocery_list.append(category) # Add to the global list 
                gkeep_grocery_list.add(category) # Add to Google Keep
         
        self.sync() # Save changes

    def generate_meals(self):
        """Check if there is enough meals available for a new generation."""

        # TODO Preserve any checked items when moving from upcoming to current

        # Find the number of meals on Upcoming Meals
        upcoming_meals_list = list(self.find(query=self.UPCOMING_MEALS_LIST))
        upcoming_meals_list = upcoming_meals_list[0]
        upcoming_meals_list_items = upcoming_meals_list.items
        num_upcoming_meals = int(len(upcoming_meals_list.items))

        # Find the number of meals on Current Meals
        current_meals_list = list(self.find(query=self.CURRENT_MEALS_LIST))
        current_meals_list = current_meals_list[0]
        current_meals_list_items = current_meals_list.items
        num_current_meals = int(len(current_meals_list.items))

        # Find the number of meals in grocery.json
        with open('data/meals.json') as file:
            meal_opts_contents = json.load(file)
            num_meal_opts = int(len(meal_opts_contents.keys()))
            meal_opt_titles = list(meal_opts_contents.keys())

        # Calculate if the desired number of meals can be generated
        # The number of meals to be generated + both lists needs to be greater than the number of options
        total_meal_qty = num_upcoming_meals + num_current_meals + self.num_meals
        if num_upcoming_meals + num_current_meals + self.num_meals > num_meal_opts:
            messagebox.showerror(title='Too Many Meals to Generate',
                                 message='The number of meals to be generated is not possible.'
                                 f' The number of meals to be generated is set to {self.num_meals}'
                                 f' Add {total_meal_qty-self.num_meals} meal options or reduce the number of meals to be generated.')
            
        # New list of meals
        new_meal_list = set() # The set removes duplicates

        # Extract texts for duplicate checking
        upcoming_texts = [item.text for item in upcoming_meals_list_items]
        current_texts = [item.text for item in current_meals_list_items]

        while len(new_meal_list) != self.num_meals: # Loop until a new meal list is full
            meal_option = random.choice(meal_opt_titles) # Select a random meal from the list
            if meal_option not in upcoming_texts and meal_option not in current_texts: # Check for repeats
                new_meal_list.add(meal_option) # Add to the set

        # Clear out the current meal list for new items
        for old_item in list(current_meals_list.items):
            old_item.delete()
            
        # Move upcoming meals into current meals
        for item_to_move in list(upcoming_meals_list.items):
            current_meals_list.add(item_to_move.text)

        # Delete the upcoming meals items to make room for new meals
        for old_item in list(upcoming_meals_list.items):
            old_item.delete()

        # Add new iems to the list
        for meal in new_meal_list:
            upcoming_meals_list.add(meal)

        self.sync() # Save changes

        new_meal_list = set() # Reset the new meal list to an empty list


    def create_grocery_list(self):
        """Create a grocery list based on the selected meals."""
        
        # Pull the items from the meal list
        upcoming_meals_list = list(self.find(query=self.UPCOMING_MEALS_LIST))
        upcoming_meals_list = upcoming_meals_list[0]
        upcoming_meals_list_items = upcoming_meals_list.items
        upcoming_meals_texts = [item.text for item in upcoming_meals_list_items]

        # Pull the items from the grocery list
        gkeep_grocery_list = list(self.find(query=self.GROCERY_STORE_LIST))[0]
        gkeep_grocery_list_items = gkeep_grocery_list.items
        gkeep_grocery_list_text = [item.text.title() for item in gkeep_grocery_list_items]

        # Meal options
        with open('data/meals.json') as file:
            meal_data = json.load(file)
            meal_data_keys = meal_data.keys() # A list of the keys

        # Grocery departments
        with open('data/grocery.json') as file:
            grocery_data = json.load(file)
            grocery_data_keys = grocery_data.keys() # A list of the keys
            
        
        temp_grocery_list = set() # Temporaily store all new groceries

        # Add the existing data (departments & groceries) to the grocery list
        # for dept_item in gkeep_grocery_list_text:
        #     all_new_groceries.append(dept_item)
      
        # Match the meal name to the key in the meals.json file to pull the ingredients needed
        for new_meal in upcoming_meals_texts:
            if new_meal in meal_data_keys:
                meal_data_values = meal_data[new_meal] # Create a list of the values
                for grocery_item in meal_data_values: 
                    temp_grocery_list.add(grocery_item) # Pull each item and add it to the all grocery list
                    
        grocery_dict = {} # Empty dict, key to be ingredient with the value to be the department

        # Match the grocery item to its respective grocery department
        for new_ingredient in temp_grocery_list: # Loop through all the new ingredients
            for key, value in grocery_data.items(): # Access the grocery dept name & items
                if new_ingredient in value: # If the new ingredient is found in the grocery items
                    grocery_dict[new_ingredient] = key # Retrieve the key of the grocery item and add it to the dict

        # Same thing but do it for the existing grocery list
        for new_ingredient in gkeep_grocery_list_text: # Loop through all the old ingredients
            for key, value in grocery_data.items(): # Access the grocery dept name & items
                if new_ingredient in value: # If the new ingredient is found in the grocery items
                    grocery_dict[new_ingredient] = key # Retrieve the key of the grocery item and add it to the dict
        
        final_grocery_list = [] # An empty list to store all new groceries
        
        # Insert the ingredient into the list in the correct location
        for dept in self.GROCERY_DEPTS:
            final_grocery_list.append(dept)
            for ingredient, ingredient_dept in grocery_dict.items():
                if ingredient_dept == dept:
                    final_grocery_list.append(ingredient)

        # Delete the items in the gkeep list & re-add the new items
        for old_item in gkeep_grocery_list_items:
            old_item.delete()
        for new_item in final_grocery_list:
            gkeep_grocery_list.add(new_item)
          
        print(final_grocery_list)
        self.sync() # Save changes


    def celebrate(self):
        # Celebrate you mother f'er, your program worked!!!
        
        soundplay.playsound('sounds/success.mp3') # Play a mp3 after the program is complete
        messagebox.showinfo(title='EZ Meal Sync Success!',
                            message='EZ Meal Sync was a success & your grocery list is ready to go!'
                            ' Kick your feet up & relax for now!')
