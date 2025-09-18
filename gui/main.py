"""temporal - trend empirical ordered analysis through likelihood
"""
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import src.gui_backend.files_processing as fp  # noqa
import src.gui_backend.functions as functions  # noqa

FILE_TYPES = [
    ("All Excel files", "*.xls;*.xlsx;*.xlsm;*.xlt;*.xltx;*.xlsb")
]
MAIN_WINDOW_XWIDTH, MAIN_WINDOW_YWIDTH = 900, 600
MAIN_WINDOW_XSHIFT, MAIN_WINDOW_YSHIFT = ..., 100

ERROR_WINDOW_XWIDTH, ERROR_WINDOW_YWIDTH = 400, 150
ERROR_WINDOW_XSHIFT, ERROR_WINDOW_YSHIFT = MAIN_WINDOW_XWIDTH // 2, 100 + MAIN_WINDOW_YWIDTH // 2


class ErrorWindow(tk.Toplevel):

    def __init__(self, error, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry(f'{ERROR_WINDOW_XWIDTH}x{ERROR_WINDOW_YWIDTH}+'
                      f'{ERROR_WINDOW_XSHIFT + self.winfo_screenwidth() // 5}+{ERROR_WINDOW_YSHIFT}')
        self.resizable(0, 0)
        self.title('Error')
        self.iconphoto(False, tk.PhotoImage(file=r'.\images\error.png'))

        t = tk.Text(self, state='normal')
        scrollx = tk.Scrollbar(self, orient='horizontal', command=t.xview)
        scrolly = tk.Scrollbar(self, orient='vertical', command=t.yview)
        t.config(xscrollcommand=scrollx.set)
        t.config(yscrollcommand=scrolly.set)

        t.pack()
        scrollx.pack()
        scrolly.pack()

        t.insert('1.0', error)
        t.config(state='disabled')


class ToolBar(tk.Menu):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)

        self.file_menu = tk.Menu(self, tearoff=0)
        self.file_menu.add_command(label="Open...", command=self.file_open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.file_exit)
        self.add_cascade(label='File', menu=self.file_menu)

        # TODO: make disable before dataframe upload
        self.tools_menu = tk.Menu(self, tearoff=0)
        self.tools_menu.add_command(label="AMT", command=self.tools_amt)
        self.add_cascade(label='Tools', menu=self.tools_menu)

    def tools_amt(self):
        self.master.amt()

    def file_exit(self):
        self.master.destroy()

    def file_open_file(self):
        self.master.process_file(filedialog.askopenfilename(filetypes=FILE_TYPES))


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # imperical identified setting
        self.geometry(f'{MAIN_WINDOW_XWIDTH}x{MAIN_WINDOW_YWIDTH}+{self.winfo_screenwidth() // 5}+{MAIN_WINDOW_YSHIFT}')
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

    def amt(self):
        # windows opening with setting
        done, data = functions.amt(self.df)
        if not done:
            # TODO: error processing
            ...

        # making new window


if __name__ == "__main__":
    a = MainApplication()
    a.mainloop()
