import webbrowser, os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as tkfont
import dotenv
from gkeep import gkeep_run

from windows.settings_page import SettingsPage

class MainPage(tk.Tk):
    """Main page."""
    def __init__(self):
        super().__init__() # Inherit tkinter

        # Icon
        icon_path = os.path.join('images', 'ez_meal_sync_logo.png')
        icon = tk.PhotoImage(file=icon_path)
        self.iconphoto(True, icon)

        self.title("EZ Meal Sync") # Page title
        
        self.padding = 5 # Default padding

        # Default font
        self.default_font = tkfont.nametofont('TkDefaultFont') # Default font name
        self.default_font.config(family='Yu Gothic', size=12)
    
        style = ttk.Style()
        style.theme_use('default') # was classic

        self.widgets() # Create the widgets
        self.mainloop() # Tkinter loop

    def widgets(self):
        frame_1 = tk.Frame(self, relief='solid', border=1, background='light coral')
        frame_1.pack(padx=self.padding, pady=self.padding)

        frame_2 = tk.Frame(self, relief="solid", border=1, background="light blue")
        frame_2.pack(padx=self.padding, pady=self.padding)

        frame_3 = tk.Frame(self, relief="solid", border=1, background='light green')
        frame_3.pack(padx=self.padding, pady=self.padding)

        # Settings button
        settings_button = tk.Button(master=frame_1, text="Settings", command=lambda: self.open_subwindow(window_name=SettingsPage))
        settings_button.pack(padx=self.padding, pady=self.padding)

        # Meal Options button
        meal_options = tk.Button(master=frame_2, text="Meal Options")
        meal_options.pack(padx=self.padding, pady=self.padding)

        # Grocery Departments button
        grocery_dept_button = tk.Button(master=frame_2, text="Grocery Departments")
        grocery_dept_button.pack(padx=self.padding, pady=self.padding)

        # Modify Current Meals button
        mod_current_meals_button = tk.Button(master=frame_2, text="Modify Current Meals")
        mod_current_meals_button.pack(padx=self.padding, pady=self.padding)

        # Generate Meals & Grocery List button
        gen_meal_button = tk.Button(master=frame_3, text="Generate Meals & Grocery List", command=lambda: self.run_meal_sync())
        gen_meal_button.pack(padx=self.padding, pady=self.padding)

        # Open Google Keep button
        open_gkeep_button = tk.Button(master=frame_3, text="Open Google Keep", command=self.open_gkeep)
        open_gkeep_button.pack(padx=self.padding, pady=self.padding)


    def open_subwindow(self, window_name):
        """Opens a subwindow."""
        window_name()

    def open_gkeep(self):
        """Open Google Keep."""
        webbrowser.open("https://keep.google.com")

    def run_meal_sync(self):
        """Runs the meal sync program."""
        verify_run = messagebox.askyesno(title='Run Meal Sync?', message='Are you sure that you want to run Meal Sync?\nThis action cannot be undone.')
        
        if verify_run == True:
            # Verify that a token is created
            # Verify email address
            # Verify that enough meals have been created to accomidate number to be generated x3
            # Run the program
            # Have a progressbar showing status
            
            gkeep_obj = gkeep_run.GKeepActions('email', token) # Create a gkeep object
            
            gkeep_obj.create_notes("Pick N' Save")