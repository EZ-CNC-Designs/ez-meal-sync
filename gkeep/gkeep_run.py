import os, tkinter as tk, time
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

        self.progress_message.update()
        time.sleep(1)
        

    def verify_data(self):
        """Runs the meal sync program."""
        verify_run = messagebox.askyesno(title='Run Meal Sync?', message='Are you sure that you want to run Meal Sync?\nThis action cannot be undone.')
        if verify_run == True:
            self.current_progress() # Open the progress window
    
            verify_token = os.getenv('GKEEP_MASTERTOKEN')
            if not verify_token:
                messagebox.showerror(title='No Master Token',
                                    message='You have not yet generated a master token.')
                return False
            
            verify_email = os.getenv('GKEEP_EMAIL')
            if not verify_email:
                messagebox.showerror(title='No Email Address',
                                    message='You have not yet entered an email address.')
                return False
                
            grocery_store_file = open('data/grocery_store.txt', 'r')
            verify_grocery_store = grocery_store_file.read()
            if not verify_grocery_store:
                messagebox.showerror(title='No Grocery Store Found',
                                    message='You have not yet entered a grocery store.')
                return False
            
            
            # Check for exceptions
            # Verify that enough meals have been created to accomidate number to be generated x3
            # Run the program
            # Have a progressbar showing status
            
            # TODO 
            # gkeep_obj = gkeep_run.GKeepActions('email', 'token') # Create a gkeep object

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

    def create_notes(self):
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
                self.progress_message.config(text=f'Creating note {note_name}')
                self.progress_message.update()
                time.sleep(.2)

        self.sync() # Save changes
           

    def adjust_grocery_list(self):
        """Set the grocery list with the correct categories."""
        grocery_lists = list(self.find(query=self.GROCERY_STORE_LIST)) # Find the grocery list
        grocery_list = grocery_lists[0]
        for category in self.GROCERY_DEPTS:
            grocery_list.add(category)
        # for line_item in grocery_list[0].items: # Access the first result
        #     print(line_item)
        #     if line_item.checked == True:
        #         print(f'{line_item} ssss') 
        self.sync()
    
class GKeepMealPlanning:
    def __init__(self):
        pass   