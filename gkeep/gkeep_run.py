import gkeepapi, gpsoauth

class GKeepGenMastToken:
    """Generate a master token to be used for Google Keep's API."""
    def __init__(self):
        pass

    def mastertoken_generator(email: str, oauth_token: str, android_id='0123456789abcdef')-> str:
        """Generates a master token to be used for Google Keep's API.
        Takes the users email address and an oauth token and returns a master token."""
    
        # Android ID is generic id as it is irrelevant
        # Exchange the OAuth token for a master token
        master_response = gpsoauth.exchange_token(email, oauth_token, android_id)

        if 'Token' in master_response:
            master_token = master_response['Token']
            # print(f"Master Token: {master_token}")
            return master_token
        else:
            # print("Error: No master token found")
            return None
        

class GKeepActions(gkeepapi.Keep):
    def __init__(self, email, master_token):
        super().__init__() # Inherit gkeepapi
        # Connect to users Google Keep
        try:
            self.authenticate(email=email, master_token=master_token)
        except ConnectionError:
            return None
        

    def create_notes(self, grocery_store):
        """Create the needed notes if they dont' exist."""
        # Set list names
        GROCERY_STORE_LIST = str(grocery_store) + " List"
        CURRENT_MEALS_LIST = "Current Meals"
        UPCOMING_MEALS_LIST = "Upcoming Meals"

        # GROCERY_DEPTS = set('Produce', 'Bakery', 'Deli', 'Meat', 'Dairy', 'Frozen',
                            # 'Health', 'Cleaning Supplies')

        new_grocery_list = self.createList(title=GROCERY_STORE_LIST,)
        new_current_meal_list = self.createList(title=CURRENT_MEALS_LIST)
        new_upcoming_meal_list = self.createList(title=UPCOMING_MEALS_LIST)

        self.sync() # Save changes


class GKeepMealPlanning:
    def __init__(self):
        pass   