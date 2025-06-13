import webbrowser, os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as tkfont
import dotenv
from gkeep import gkeep_run
from windows.new_user_message import NewUser
from windows.settings_window import SettingsWindow
from windows.meal_library_window import MealLibraryWindow
from windows.grocery_dept_window import GroceryDeptWindow
from windows.modify_meal_list import ModifyMealList

class MainWindow(tk.Tk):
    """Main page."""
    def __init__(self):
        super().__init__() # Inherit tkinter

        dotenv.load_dotenv('data/.env')

        # Icon
        icon_path = os.path.join('images', 'ez_meal_sync_logo.png')
        icon = tk.PhotoImage(file=icon_path)
        self.iconphoto(True, icon)

        self.title("EZ Meal Sync") # Page title
        
        self.padding = 5 # Default padding

        # Default font
        self.default_font = tkfont.nametofont('TkDefaultFont') # Default font name
        self.default_font.config(family='Yu Gothic', size=12)
    
        # style = ttk.Style()
        # style.theme_use('default')

        self.widgets() # Create the widgets
        NewUser()
        self.mainloop() # Tkinter loop

    def widgets(self):
        """Create the widgets."""

        frame_1 = tk.Frame(self, relief='solid', border=1, background='misty rose')
        frame_1.pack(padx=self.padding, pady=self.padding)

        frame_2 = tk.Frame(self, relief="solid", border=1, background='light goldenrod yellow')
        frame_2.pack(padx=self.padding, pady=self.padding)

        frame_3 = tk.Frame(self, relief="solid", border=1, background='light cyan')
        frame_3.pack(padx=self.padding, pady=self.padding)

        # Settings button
        settings_button = tk.Button(master=frame_1, text="Settings", command=lambda: SettingsWindow())
        settings_button.pack(padx=self.padding, pady=self.padding)

        # Meal Library button
        meal_library = tk.Button(master=frame_2, text="Meal Library", command=lambda: MealLibraryWindow())
        meal_library.pack(padx=self.padding, pady=self.padding)

        # Grocery Departments button
        grocery_dept_button = tk.Button(master=frame_2, text="Grocery Departments", command=lambda: GroceryDeptWindow())
        grocery_dept_button.pack(padx=self.padding, pady=self.padding)

        # Modify Current Meals button
        mod_meal_list_button = tk.Button(master=frame_2, text="Modify Meal List", command=lambda: ModifyMealList())
        mod_meal_list_button.pack(padx=self.padding, pady=self.padding)

        # Generate Meals & Grocery List button
        gen_meal_button = tk.Button(master=frame_3, text="Generate Meals & Grocery List", command=lambda: self.run_meal_sync())
        gen_meal_button.pack(padx=self.padding, pady=self.padding)

        # Open Google Keep button
        open_gkeep_button = tk.Button(master=frame_3, text="Open Google Keep", command=lambda: webbrowser.open("https://keep.google.com"))
        open_gkeep_button.pack(padx=self.padding, pady=self.padding)


    def run_meal_sync(self):
        """Runs the meal sync program."""
        verify_run = messagebox.askyesno(title='Run Meal Sync?', message='Are you sure that you want to run Meal Sync?\nThis action cannot be undone.')
        
        if verify_run == True:
            verify_token = os.getenv('GKEEP_MASTERTOKEN')
            if not verify_token:
                messagebox.showerror(title='No Master Token',
                                    message='You have not yet generated a master token.')
            verify_email = os.getenv('GKEEP_EMAIL')
            if not verify_email:
                messagebox.showerror(title='No Email Address',
                                    message='You have not yet entered an email address.')
                
            grocery_store_file = open('data/grocery_store.txt', 'r')
            verify_grocery_store = grocery_store_file.read()
            if not verify_grocery_store:
                messagebox.showerror(title='No Grocery Store Found',
                                    message='You have not yet entered a grocery store.')


            # Check for exceptions
            # Verify that enough meals have been created to accomidate number to be generated x3
            # Run the program
            # Have a progressbar showing status
            
            # TODO 
            gkeep_obj = gkeep_run.GKeepActions('email', 'token') # Create a gkeep object
            