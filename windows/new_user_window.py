import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import dotenv

class NewUser():
    """Instructs a new user what to do when first opening the window."""
    def __init__(self):
        dotenv.load_dotenv('data/.env')
        master_token = os.getenv('GKEEP_MASTERTOKEN')
        if not master_token:
            self.new_user_message()

    def new_user_message(self):
        """Display a message to the new user."""
        message = (
            "Welcome to EZ Meal Sync!\n\n"
            "This app helps you plan meals by randomly picking meals from your list, then creating "
            "a grocery list with the needed ingredients. It syncs everything to Google Keep so you "
            "can access it easily while shopping.\n\n"
            "To get started, you'll need a Google account and a master token. If you're not sure how "
            "to get one, follow the instructions here:\n"
            "https://github.com/EZ-CNC-Designs/ez-meal-sync/blob/main/README.md\n\n"
            "Once you have your token, enter your grocery store’s name and choose how many meals you "
            "want on each list. Then start adding meals and ingredients to your menu.\n\n"
            "Tip: Make sure your menu has at least 3 times more meals than you plan to generate in a list."
            )


        messagebox.showinfo(title='Welcome New User!', message=message)
