"""temporal - trend empirical ordered analysis through likelihood
"""
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import src.gui_backend.files_processing as fp


FILE_TYPES = [
    ("All Excel files", "*.xls;*.xlsx;*.xlsm;*.xlt;*.xltx;*.xlsb")
]


class ToolBar(tk.Menu):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)

        self.file_menu = tk.Menu(self, tearoff=0)
        self.file_menu.add_command(label="Open...", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit)
        self.add_cascade(label='File', menu=self.file_menu)

    def exit(self):
        self.master.destroy()

    def open_file(self):
        self.master.process_file(filedialog.askopenfilename(filetypes=FILE_TYPES))


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # imperical identified setting
        self.geometry(f'900x600+{self.winfo_screenwidth() // 5}+100')
        self.resizable(0, 0)
        self.title('temporal')
        self.iconphoto(False, tk.PhotoImage(file=r'.\images\title_image.png'))

        # widgets creating
        self.main_window = tk.Frame(self)
        self.main_window.pack(fill=tk.BOTH, expand=True)

        # widgets launcing
        main_menubar = ToolBar(self)
        self.config(menu=main_menubar)

    def display_data(self):
        """Displays recieved data in the table
        """
        table = ttk.Treeview(self, columns=("#", "Column", "Not null count / All"), show='headings')
        table.heading('#', text="#")
        table.heading('Column', text="Column")
        table.heading('Not null count / All', text="Not null count / All")

        for i, col in enumerate(self.df):
            table.insert(parent='', index=i, values=(i, col, f"{(~self.df[col].isna()).shape[0]} / {self.df.shape[0]}"))
        table.place(x=0, y=0)

    def process_file(self, path: str):
        """Launches a function of data processing and then launches a function of data displaying

        Args:
            path (str): path to file
        """
        self.df = fp.process_app_file(path)
        self.display_data()


if __name__ == "__main__":
    a = MainApplication()
    a.mainloop()
