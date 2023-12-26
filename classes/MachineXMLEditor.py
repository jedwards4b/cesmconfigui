import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from classes.CIME_interface import CIME_interface

debug = True

class MachineXMLEditor(ttk.Frame):
    def __init__(self, root, machine, cime):
        super().__init__(root)

        self.selected_machine_name = machine
        self.cime = cime
        # Create a scrollable frame
#        self.scrollable_frame = ttk.Frame(self)
        self.canvas = tk.Canvas(self, width=root.winfo_width(), height=root.winfo_height())
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Create a frame inside the canvas for the grid
        self.content_frame = ttk.Frame(self)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Create the grid layout
        self.grid_layout = ttk.Frame(self.content_frame)
        self.grid_layout.pack(fill="both", expand=True)

        ttk.Label(self.grid_layout, text="Machine:").grid(row=0,column=0)
        ttk.Label(self.grid_layout, text=machine).grid(row=0,column=1)

        ttk.Label(self.grid_layout, text="Description:").grid(row=1, column=0)
        self.desc_entry = ttk.Entry(self.grid_layout)
        self.desc_entry.insert(0, self.cime.machinesxml.get_value("DESC"))
        self.desc_entry.grid(row=1, column=1, sticky="ew", columnspan=2)

        ttk.Label(self.grid_layout, text="Operating System:").grid(row=2, column=0)
        self.processor_type_list = ["Linux", "CNL", "Darwin"]
        self.processor_type_combobox = ttk.Combobox(self.grid_layout, values=self.processor_type_list)
        self.processor_type_combobox.grid(row=2, column=1)
        self.processor_type_combobox.current(self.processor_type_list.index(self.cime.machinesxml.get_value("OS")))

        def select_cime_output_root():
            self.cime_output_root_entry.delete(0, tk.END)
            self.cime_output_root_entry.insert(0, filedialog.askdirectory(initialdir=self.cime_output_root))

        ttk.Label(self.grid_layout, text="CIME OUTPUT ROOT:").grid(row=3, column=0)
        self.cime_output_root = self.cime.machinesxml.get_value("CIME_OUTPUT_ROOT")
        self.cime_output_root_entry = tk.Entry(self.grid_layout)
        self.cime_output_root_entry.insert(0, self.cime_output_root)
        self.cime_output_root_entry.grid(row=3, column=1)
        self.select_dir_button = tk.Button(self.grid_layout, text="Browse...", command=select_cime_output_root)
        self.select_dir_button.grid(row=3, column=2, sticky="e")


        self.pack()

        
        #        self.grid()
#        self.label = tk.Label(self, text=f"Machine: {machine}")
#        self.label.grid(row=0, column=0, sticky="N")
#        self.grid_columnconfigure(0, weight=1)
#        self.grid_rowconfigure(2, weight=1)

#        label = tk.Label(self, text="Description:")
#        entry = tk.Entry(self)
#        entry.insert(0, self.cime.machinesxml.get_value("DESC"))
#        label.grid(row=1, column=0, sticky="w")
#        entry.grid(row=1, column=1, sticky="nsew")
        
