#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  This program requires python 3.6 or newer with the BeautifulSoup package to run

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, showerror
import sys
import os
import json
from classes.CIME_interface import CIME_interface

# default options
opt = {
    # Todo: make this general
    'dir': "/glade/u/home/jedwards/sandboxes/cesm2_x_alpha/ccs_config/machines", # last seen directory
    'filename': "config_machines.xml",
    'geometry': "350x550",
    'save_position': True, # save the geometry and position of the window and restore on next load
#    'formats': 'config_machines.xml', # extensions of files to be listed; space delimited
#    'entrybox_width': 25,  # width of the entry boxes
#    'output_encoding': 'autodetect', # any valid encoding ('utf-8', 'utf-16le', etc) or autodetect.
    'backup_ext': '.bak', # extension of backed up files. Use something not in 'formats' to prevent backups from showing in the dropdown list.
    }
# load global options dictionary
opt_fn = "cimeconfigurator_options.json"
try:
    with open(opt_fn) as f:
        opt.update(json.load(f))
except Exception as e:
    print("default options used due to", e)


class XMLMachines(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.cime = CIME_interface(cimeroot="/glade/u/home/jedwards/sandboxes/cesm2_x_alpha/cime")
        filename = self.cime.get_machines_file()
        root.title("CIME Configurator")
        root.geometry(opt["geometry"])
        root.protocol('WM_DELETE_WINDOW', self._quit)
        self.root = root
        self.data_frame = tk.Frame(self)
        scrollbar = ttk.Scrollbar(self.root)
        self.display = ttk.Treeview(self.root, yscrollcommand=scrollbar.set, show="tree", selectmode="browse")
        scrollbar.configure(command=self.display.yview)
        scrollbar.pack(side="right", fill="y")
        self.display.pack(expand=True, fill=tk.BOTH)

        

    def _quit(self):
        if opt.get('save_position'):
            opt['geometry'] = self.root.geometry()
        else:
            # strip the position information; keep only the size information
            opt['geometry'] = self.root.geometry().split('+')[0]
        self.root.destroy()

        
def main():
    root = tk.Tk()
    window = XMLMachines(root)
    window.pack(fill=tk.BOTH, expand=True)
    if len(sys.argv) > 1:
        window.top.load_path(" ".join(sys.argv[1:]))
    root.mainloop()
    with open(opt_fn, 'w') as f:
        json.dump(opt, f, indent=2)



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        showerror("Fatal error!", "CIME Editor crashed.\n\n"+str(e))
        raise

