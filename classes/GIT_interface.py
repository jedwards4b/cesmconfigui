import os
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from git import Repo

debug = True

class ResizingFrame(tk.Frame):
    def __init__(self, master, entry):
        super().__init__(master)
        self.entry = entry
        self.entry.pack(fill="x", expand=True)

    def update_width(self):
        width = self.entry.winfo_reqwidth() + 10
        self.config(width=width)

class GIT_interface(tk.Frame):
    def __init__(self, root, repo_list):
        super().__init__(root)
        self.repo_list = repo_list
        self.clone_successful = False
        initial_repo_url = repo_list[0]
        self.local_dir = os.path.join(os.getcwd(), "cesm")

        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Labels and entries
        self.repo_url_label = tk.Label(self, text="Git Repository:")
        self.repo_url_combo = ttk.Combobox(self)
        self.repo_url_combo["values"] = [initial_repo_url]  # Pre-populate with initial URL
        self.repo_url_combo.set(initial_repo_url)  # Set initial selection

        self.local_dir_label = tk.Label(self, text="Local Directory:")
        self.local_dir_entry = tk.Entry(self)
        self.local_dir_entry.insert(0, self.local_dir)  # Set initial directory

        # Progress bar and label
#        self.progress_bar = ttk.Progressbar(self, orient="horizontal")
#        self.progress_label = ttk.Label(self, text="Downloading...")

        # Grid placement
        self.repo_url_label.grid(row=0, column=0, sticky="w")
        self.repo_url_combo.grid(row=0, column=1, sticky="nsew")
        self.local_dir_label.grid(row=1, column=0, sticky="w")
        self.local_dir_entry.grid(row=1, column=1, sticky="nsew")
#        self.progress_bar.grid(row=3, columnspan=2, sticky="nsew")
#        self.progress_label.grid(row=4, columnspan=2, sticky="nsew")

        
        # Adjust width based on initial values
        self.repo_url_combo.config(width=len(initial_repo_url) + 5)  # Add padding
        self.local_dir_entry.config(width=len(self.local_dir) + 5)

        # Button functions (same as previous version)
        def select_dir():
            self.local_dir_entry.delete(0, tk.END)
            self.local_dir_entry.insert(0, filedialog.askdirectory())

        def clone_repo():
            selected_repo_url = self.repo_url_combo.get()
            selected_repo_dir = self.repo_list
            self.local_dir = self.local_dir_entry.get()

            try:
                self.clone_repo(selected_repo_url, self.local_dir)
                self.clone_successful = True
                tk.messagebox.showinfo("Success", f"Repository cloned to '{self.local_dir}'")
                os.environ['CIMEROOT'] = os.path.join(self.local_dir, "cime")
                
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error cloning repository: {e}")

        # Buttons and grid placement
        self.select_dir_button = tk.Button(self, text="Browse...", command=select_dir)
        self.select_dir_button.grid(row=1, column=2, sticky="e")

        self.clone_button = tk.Button(self, text="Clone", command=clone_repo)
        self.clone_button.grid(row=2, column=1, sticky="nsew")

        self.pack()

        
    def clone_repo(self, repo_name, local_name):
#        self.progress_bar["maximum"] = 100
#        self.progress_bar["value"] = 0
#        self.progress_label["text"] = "Downloading..."
#        Repo.clone_from(repo_name, local_name, progress=self._update_progress_bar)
        Repo.clone_from(repo_name, local_name)
        _LIBDIR = os.path.join(self.local_dir,"manic")
        sys.path.append(_LIBDIR)
        import_module('manic')
        manic.checkout.main()


    def _update_progress_bar(self, progress, total):
        self.progress_bar["maximum"] = total
        self.progress_bar["value"] = progress
        percent_complete = int(progress / total * 100)
        self.progress_label["text"] = f"Downloading... ({percent_complete}%)"

    
    
