import os, pathlib
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import dotenv
from gkeep.gkeep_run import GKeepGenMastToken


class SettingsWindow(tk.Toplevel):
    def __init__(self):
        super().__init__() # Inheritance

        self.title("Settings") # Name of window
        self.padding = 5 # Standard padding

        # If a .env file doesn't exist, create one with variable names
        if not pathlib.Path('data/.env').exists():
            with open(file='data/.env', mode='w') as file:
                file.write('GKEEP_EMAIL=\nGKEEP_MASTERTOKEN=')
            
            dotenv.load_dotenv(dotenv_path='data/.env')
            self.widgets() # Create the widgets

        else:
            dotenv.load_dotenv(dotenv_path='data/.env')
            self.widgets()


    def widgets(self):
        # Frame 1
        frame_1 = tk.Frame(master=self, relief='solid', border=1, background='misty rose')
        frame_1.pack(padx=self.padding, pady=self.padding)

        # Frame 2
        frame_2 = tk.Frame(master=self, relief='solid', border=1, background='light goldenrod yellow')
        frame_2.pack(padx=self.padding, pady=self.padding)

        # Frame 3
        frame_3 = tk.Frame(master=self, relief='solid', border=1, background='light cyan')
        frame_3.pack(padx=self.padding, pady=self.padding)

        # Email Prompt Text
        email_prompt_text = tk.Label(master=frame_1, text='Email Address', background='misty rose')
        email_prompt_text.pack(padx=self.padding, pady=self.padding)

        # Email Entry
        # Load the contents
        email_entry_var = tk.StringVar(value=os.getenv('GKEEP_EMAIL'))
        # Create the widget
        email_entry = tk.Entry(master=frame_1, font=('Yu Gothic', 12), textvariable=email_entry_var)
        email_entry.pack(padx=self.padding, pady=self.padding)
        # Save the contents
        email_entry.bind('<KeyRelease>', lambda event: self.save_env_input(email_entry.get(), 'GKEEP_EMAIL'))

        # Oauth Token Text
        oauth_token_text = tk.Label(master=frame_1, text='OAuth Token', background='misty rose')
        oauth_token_text.pack(padx=self.padding, pady=self.padding)

        # Oauth Token Entry        
        oauth_token_entry = tk.Entry(master=frame_1, font=('Yu Gothic', 12))
        oauth_token_entry.pack(padx=self.padding, pady=self.padding)

        # Generate Master Token Button
        gen_master_token_button = tk.Button(master=frame_1, text='Generate Master Token',
                                            command=lambda: self.gen_master_token(oauth_token=oauth_token_entry.get()))
        gen_master_token_button.pack(padx=self.padding, pady=self.padding)

        # Number of Meals Label
        num_meals_label = tk.Label(master=frame_2, text='Number of Meals to be Generated', background='light goldenrod yellow')
        num_meals_label.pack(padx=self.padding, pady=self.padding)

        # Number of Meals Entry
        # Load the input if exists
        meal_qty_file_path = 'data/meal_qty.txt'
        meal_qty_var = self.set_var(meal_qty_file_path)
        # Create the Widgets
        num_meals_entry = tk.Entry(master=frame_2, font=('Yu Gothic', 12), textvariable=meal_qty_var)
        num_meals_entry.pack(padx=self.padding, pady=self.padding)
        # Save the entry
        num_meals_entry.bind('<KeyRelease>', lambda event: self.save_input(input=num_meals_entry.get(),
                                                                           file_path=meal_qty_file_path))

        # Grocery Store Label
        grocery_store_label = tk.Label(master=frame_3, text='Default Grocery Store', background='light cyan')
        grocery_store_label.pack(padx=self.padding, pady=self.padding)

        # Grocery Store Entry
        # Load input if exists
        grocery_store_file_path = 'data/grocery_store.txt'
        grocery_store_var = self.set_var(file_path=grocery_store_file_path)
        # Create the widget
        grocery_store_entry = tk.Entry(master=frame_3, font=('Yu Gothic', 12), textvariable=grocery_store_var)
        grocery_store_entry.pack(padx=self.padding, pady=self.padding)
        # Save the input
        grocery_store_entry.bind('<KeyRelease>', lambda event: self.save_input(input=grocery_store_entry.get(),
                                                                         file_path=grocery_store_file_path))


    def set_var(self, file_path):
        """Set a entry variable."""
        with open(file_path, 'r') as file:
            contents = file.read()
        var_to_set = tk.StringVar()
        var_to_set.set(contents)
        return var_to_set
    

    def save_input(self, input, file_path):
        """Saves an entry input."""
        with open(file_path, 'w') as file:
            file.write(input)


    def save_env_input(self, input, variable_name):
        """Saves an entry input to a .env."""
        dotenv.set_key('data/.env', variable_name, input)
        dotenv.load_dotenv(dotenv_path='data/.env', override=True)
       

    def gen_master_token(self, oauth_token):
        """Generates a master token for Google Keep."""
        
        email_address = os.getenv('GKEEP_EMAIL')    
        
        if not email_address: # Verify an email address is given
            messagebox.showerror(title='Missing Email Address',
                              message='You have not entered an email address.\nA master token cannot be generated.')
            
        elif not oauth_token: # Verify an oauth token is given
            messagebox.showerror(title='Missing Oauth Token',
                              message='You have not entered an oauth token.\nA master token cannot be generated.')
            
        else: # Prompt to continue
            verify_gen_token = messagebox.askyesno(title='Generate Master Token?',
                                message='Are you sure you want to generate a new master token?\nA new token is only needed initially or if your Google password changes.')
            
            if verify_gen_token == True:
                # Generate a master token 
                gen_token = GKeepGenMastToken().mastertoken_generator(email=email_address, oauth_token=oauth_token)
                if not gen_token:
                    messagebox.showerror(title='Master Token Generation Failed',
                                         message='The attempt to generate a master token failed.\nVerify that your email & oauth token is correct.')

                elif gen_token:
                    dotenv.set_key('data/.env', 'GKEEP_MASTERTOKEN', gen_token)
                    messagebox.showinfo(title='Success Generating Master Token!',
                                     message='A master token has been generated & saved.\nYou can now run the Meal Sync.')
        