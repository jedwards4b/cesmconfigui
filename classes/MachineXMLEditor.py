import tkinter as tk
from tkinter import ttk
from classes.CIME_interface import CIME_interface

debug = True

class MachineXMLEditor(tk.Frame):
    def __init__(self, root, machine):
        super().__init__(root)
        self.grid()
        self.label = tk.Label(self, text=f"Machine: {machine}")
        self.label.grid(row=0, column=0, sticky="NSEW")
        self.tkraise()
