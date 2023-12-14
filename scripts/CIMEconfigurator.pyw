import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd   
import json
import os
from classes.CIME_interface import CIME_interface
from classes.MachineXMLEditor import MachineXMLEditor
from classes.GIT_interface import GIT_interface

debug = True

opt = {
    'config_machines':  "/glade/u/home/jedwards/sandboxes/cesm2_x_alpha/ccs_config/machines/config_machines.xml", # last seen directory
    'cime_root': os.getenv("CIMEROOT"),
    'cesm_repo_list': ["https://github.com/ESCOMP/cesm"],
    'root_geometry': '1000x350'
}

class CESMConfigMachineEditor(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.grid()
        root.geometry(opt['root_geometry'])
        self.root = root
        self.filename = opt['config_machines']
        self.cimeroot = opt['cime_root']

        if debug: print(f"cime_root {self.cimeroot}, config_machines {self.filename}")
        self.machine_selection_frame = tk.Frame(self)
        self.machine_selection_frame.grid()
        
        entrywidth = max(len(self.filename), len(self.cimeroot))
        
        # Frame for selecting the CIME_ROOT directory
        self.cime_root_selection_frame = tk.Frame(self.machine_selection_frame)
        self.cime_root_label = tk.Label(self.cime_root_selection_frame, text="CIME ROOT Directory:")
        self.cime_root_label.grid(row=0, column=0, sticky='W')
        self.cime_root_entry = tk.Entry(self.cime_root_selection_frame, width=entrywidth)
        self.cime_root_entry.grid(row=0, column=1, sticky='EW')
        self.cime_root_button = tk.Button(self.cime_root_selection_frame, text="Select CIME_ROOT", command=self.select_cime_root)
        self.cime_root_button.grid(row=0, column=4, sticky='E')
        self.cime_root_selection_frame.grid(row=0, column=0, sticky='NSEW')
        self.cime_root_entry.delete(0, tk.END)
        self.cime_root_entry.insert(0, opt['cime_root'])
        
        # Frame for selecting the config_machines.xml file
        self.file_selection_frame = tk.Frame(self.machine_selection_frame)
        self.file_selection_frame.grid(row=1, column=0, sticky='NSEW')

        self.filename_label = tk.Label(self.file_selection_frame, text="Config Machines XML File:")
        self.filename_label.grid(row=0, column=0, sticky='W')

        self.filename_entry = tk.Entry(self.file_selection_frame, width=entrywidth)
        self.filename_entry.grid(row=0, column=1, sticky='EW')
        self.filename_entry.delete(0, tk.END)

        self.filename_entry.insert(0, self.filename)

        self.select_file_button = tk.Button(self.file_selection_frame, text="Select File", command=self.select_file)
        self.select_file_button.grid(row=0, column=2, sticky='E')

        self.machinelist_frame = tk.Frame(self.machine_selection_frame)
        scrollbar = ttk.Scrollbar(self.machinelist_frame)
        self.display = ttk.Treeview(self.machinelist_frame, yscrollcommand=scrollbar.set, show="tree", selectmode="browse")
        self.get_machineslist()
        scrollbar.configure(command=self.display.yview)
        scrollbar.pack(side="right", fill='y')
        self.display.pack(expand=True, side=tk.BOTTOM, fill=tk.BOTH)
        self.machinelist_frame.grid(row=2,column=0, sticky='S')
        self.define_buttons()
        
        
    def get_machineslist(self):
        self.cime = CIME_interface(cimeroot=self.cimeroot)
        self.machineslist = self.cime.get_machines(self.filename)
        if debug: print(f"List of machines: {self.machineslist}")
        for mach in self.machineslist:
            self.display.insert("", "end", text=mach)
        

        
        # Frame for editing machine information
        # self.machine_info_frame = tk.Frame(self)
        # self.machine_info_frame.grid(row=2, column=0, columnspan=2)

        # self.machine_name_label = tk.Label(self.machine_info_frame, text="Machine Name:")
        # self.machine_name_label.grid(row=0, column=0)
        # self.machine_name_entry = tk.Entry(self.machine_info_frame)
        # self.machine_name_entry.grid(row=0, column=1)

        # self.machine_type_label = tk.Label(self.machine_info_frame, text="Machine Type:")
        # self.machine_type_label.grid(row=1, column=0)
        # self.machine_type_entry = tk.Entry(self.machine_info_frame)
        # self.machine_type_entry.grid(row=1, column=1)

        # self.machine_cores_label = tk.Label(self.machine_info_frame, text="Machine Cores:")
        # self.machine_cores_label.grid(row=2, column=0)
        # self.machine_cores_entry = tk.Entry(self.machine_info_frame)
        # self.machine_cores_entry.grid(row=2, column=1)

#        self.save_button = tk.Button(self.machine_info_frame, text="Save Changes", command=self.save_changes)
#        self.save_button.grid(row=3, column=0, columnspan=2)

    def select_file(self):
        filename = fd.askopenfilename(filetypes=[("XML Files", "*.xml")])
        if filename:
            self.filename = filename
            self.filename_entry.delete(0, tk.END)
        self.filename_entry.insert(0, filename)
        # Load the selected file's contents
        self.get_machineslist(filename)

    def select_cime_root(self):
        if opt['cime_root']:
            initial_dir = opt['cime_root']
        else:
            initial_dir = os.cwd()
        cime_root = fd.askdirectory(mustexist=True, initialdir=initial_dir)
        if cime_root:
            self.cime_root = cime_root
            self.cime_root_entry.delete(0, tk.END)
        self.cime_root_entry.insert(0, filename)

        # Load the selected file's contents
        #        self.file = File(filename, "r")
        #        self.machine_element = self.file.get_root_element("machine")
    def saveall(self):
        """ Write updated XML object to file """
        
        if debug: print("saveall called")

    def cancel(self):
        """ Cancel the changes to config_machines """
        
        if debug: print("cancel called")

    def new_machine(self):
        """ Copy the example machine description into a new machine name """
        
        if debug: print("new machine called")

    def edit_machine(self):
        """ Edit the selected machine description """
        machine = self.display.item(self.display.selection()[0], option="text")
        if debug: print(f"edit machine called, machine is {machine}")
        self.ew = MachineXMLEditor(self, machine)


        #        XMLMachineEditor(ew, self.bsmachines[machine])

    def copy_machine(self):
        """ Copy the given machine description into a new machnine name """
        
        machine = self.display.item(self.display.selection()[0], option="text")
        if debug: print(f"copy machine called, machine is {machine}")
        new_machine_name = tk.simpledialog.askstring(title="Copy", prompt="Enter the new machine name:")
        if debug: print(f"new_machine is {new_machine_name}")
        if new_machine_name in self.machineslist:
            print(f"ERROR: match to name in list")
        elif new_machine_name:
            self.cime.copy_machine(machine, new_machine_name)
            self.machineslist.append(new_machine_name)
            self.display.insert("", "end", text=new_machine_name)
            self.display.selection_set(self.display.get_children()[-1])
            self.edit_machine()
            
    def delete_machine(self):
        """ Delete the given machine - eventually this should apply to all cesm config xml files """
        machine = self.display.item(self.display.selection()[0], option="text")
        if debug: print(f"delete machine called, machine is {machine}")
        
        self.display.delete(self.display.focus())
        self.bsmachines[machine].decompose()
        del self.bsmachines[machine]

    def define_buttons(self):
        frame = ttk.Frame(self.machine_selection_frame)
        frame.columnconfigure(0, weight=1)
        newmach = ttk.Button(frame, text="New", command=self.new_machine)
        editmach = ttk.Button(frame, text="Edit", command=self.edit_machine)
        copymach = ttk.Button(frame, text="Copy", command=self.copy_machine)
        deletemach = ttk.Button(frame, text="Delete", command=self.delete_machine)
        saveall = ttk.Button(frame, text="Save", command=self.saveall)
        cancel = ttk.Button(frame, text="Cancel", command=self.cancel)
        next_row = self.machine_selection_frame.grid_size()[1]
        frame.grid(row=next_row,column=0)
        newmach.grid(row=0,column=0)
        editmach.grid(row=0,column=1)
        copymach.grid(row=0,column=2)
        deletemach.grid(row=0,column=3)
        saveall.grid(row=0,column=5)
        cancel.grid(row=0,column=6)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("CIME XML Configurator")
    cimeeditor = None
    if not opt['cime_root'] and os.path.isdir(os.path.join(os.getcwd(),'cesm','cime')):
        opt['cime_root'] = os.path.join(os.getcwd(),'cesm', 'cime')

    if opt['cime_root']:
        os.environ['CIMEROOT'] = opt['cime_root']
        cimeeditor = CESMConfigMachineEditor(root)
    else:
        gitimport = GIT_interface(root, opt['cesm_repo_list'])
        gitimport.mainloop()  # Wait for GIT interface to finish
        if gitimport.clone_successful:  # Check if cloning was successful
            cimeeditor = CESMConfigMachineEditor(root)

    if cimeeditor:  # Only if CESM editor is created
        cimeeditor.mainloop()        
        
