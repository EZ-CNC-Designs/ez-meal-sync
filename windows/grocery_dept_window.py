import tkinter as tk
from tkinter import ttk

class GroceryDeptWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Grocery Departments')