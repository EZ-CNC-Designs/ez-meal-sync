import tkinter as tk, json
from tkinter import ttk


class MealLibraryWindow(tk.Toplevel):
    def __init__(self):
        super().__init__() # Inheritance

        self.title('Meal Options')
        self.padding = 5
        self.widgets()
        self.load_meals()

    def widgets(self):
        frame_1 = tk.Frame(master=self, relief='solid', border=1, background='misty rose')
        frame_1.pack(padx=self.padding, pady=self.padding)

        frame_2 = tk.Frame(master=self, relief='solid', border=1, background='light goldenrod yellow')
        frame_2.pack(padx=self.padding, pady=self.padding)

        meal_options_label = tk.Label(master=frame_1, text='Meal Options', background='misty rose')
        meal_options_label.pack(padx=self.padding, pady=self.padding) 

        meal_titles = self.load_meals()
        ingredient_var = ''
        meal_combobox = ttk.Combobox(master=frame_1, values=meal_titles)
        meal_combobox.pack(padx=self.padding, pady=self.padding)

        ingredients_label = tk.Label(master=frame_1, text="Ingredients")
        ingredients_label.pack(padx=self.padding, pady=self.padding)

        text = tk.Label(master=frame_2, text='Create Meal', background='light goldenrod yellow')
        text.pack()

        

    def load_meals(self):
        with open(file='data/meals.json', mode='r') as file:
            contents = json.load(file)
            return list(contents.keys())
        # Retrieve the titles

    def load_ingredients(self):
        pass