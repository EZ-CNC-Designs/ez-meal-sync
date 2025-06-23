import os, tkinter as tk, time, json
from tkinter import ttk
import gkeepapi, gpsoauth, dotenv
from gkeepapi.exception import LoginException
from typing import Optional
from tkinter import messagebox

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

        self.GROCERY_DEPTS = set(['Produce', 'Bakery', 'Deli', 'Meat', 'Dairy', 'Frozen',
                            'Health', 'Cleaning Supplies'])

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

    def verify_num_meals(self):
        """Check if there is enough meals available for a new generation."""

        # Find the number of meals on Upcoming Meals
        upcoming_meals_list = list(self.find(query=self.UPCOMING_MEALS_LIST))
        upcoming_meals_list = upcoming_meals_list[0]
        num_upcoming_meals = int(len(upcoming_meals_list.items))

        # Find the number of meals on Current Meals
        current_meals_list = list(self.find(query=self.CURRENT_MEALS_LIST))
        current_meals_list = current_meals_list[0]
        num_current_meals = int(len(current_meals_list.items))

        # Find the number of meals in grocery.json
        with open('data/meals.json') as file:
            meal_opts_contents = json.load(file)
            num_meal_opts = int(len(meal_opts_contents.keys()))

        # Calculate if the desired number of meals can be generated
        # The number of meals to be generated + both lists needs to be greater than the number of options
        total_meal_qty = num_upcoming_meals + num_current_meals + self.num_meals
        print(num_meal_opts)
        if num_upcoming_meals + num_current_meals + self.num_meals > num_meal_opts:
            messagebox.showerror(title='Too Many Meals to Generate',
                                 message='The number of meals to be generated is not possible.'
                                 f' The number of meals to be generated is set to {self.num_meals}'
                                 f' Add {total_meal_qty-self.num_meals} meal options or reduce the number of meals to be generated.')
        
       
        # Check for any other numbering conflicts

        # Pull the 2 meal options lists
        # Generate a new list of meals without repeats
        # Push the new meal list, move the upcoming meal list, do nothing with the old list
