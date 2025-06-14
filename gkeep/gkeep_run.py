import os
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

        
        GROCERY_DEPTS = set(['Produce', 'Bakery', 'Deli', 'Meat', 'Dairy', 'Frozen',
                            'Health', 'Cleaning Supplies'])

        grocery_store_file = open('data/grocery_store.txt', 'r')
        self.grocery_store_name = grocery_store_file.read()
        # Set list names
        self.GROCERY_STORE_LIST = str(self.grocery_store_name) + " List"
        self.CURRENT_MEALS_LIST = "Current Meals"
        self.UPCOMING_MEALS_LIST = "Upcoming Meals"
        

    def verify_data(self):
        """Runs the meal sync program."""
        verify_run = messagebox.askyesno(title='Run Meal Sync?', message='Are you sure that you want to run Meal Sync?\nThis action cannot be undone.')
        if verify_run == True:
    
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

            # GROCERY_DEPTS = set('Produce', 'Bakery', 'Deli', 'Meat', 'Dairy', 'Frozen',
                                # 'Health', 'Cleaning Supplies')

            self.new_grocery_store_list = self.createList(title=self.GROCERY_STORE_LIST,)
            self.new_current_meal_list = self.createList(title=self.CURRENT_MEALS_LIST)
            self.new_upcoming_meal_list = self.createList(title=self.UPCOMING_MEALS_LIST)

            self.sync() # Save changes
class GKeepMealPlanning:
    def __init__(self):
        pass   