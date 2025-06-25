import webbrowser, os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as tkfont
import dotenv
from gkeep.gkeep_run import GKeepActions
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
        gen_meal_button = tk.Button(master=frame_3, text="Generate Meals & Grocery List",
                                    command=lambda: self.run_meal_sync())
        gen_meal_button.pack(padx=self.padding, pady=self.padding)

        # Open Google Keep button
        open_gkeep_button = tk.Button(master=frame_3, text="Open Google Keep", command=lambda: webbrowser.open("https://keep.google.com"))
        open_gkeep_button.pack(padx=self.padding, pady=self.padding)

    def run_meal_sync(self):
        """Run the meal sync program."""
        run = GKeepActions()
        
        # TODO add error handling

        verify = run.verify_data()
        if verify != False:
            run.user_login() # Login
            run.create_lists() # Create missing lists
            run.adjust_grocery_list() # Add missing categories
            run.generate_meals() # Generate new meals
            run.create_grocery_list() # Create the grocery list
            run.celebrate() # Play end sound
                