""""""
import tkinter as tk
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
# HACK: Manually add the project root to sys.path to enable relative imports
# when running 'temporal.py' directly from its location.
sys.path.append(os.path.dirname(SCRIPT_DIR))


MAIN_WINDOW_XWIDTH, MAIN_WINDOW_YWIDTH = 900, 600
MAIN_WINDOW_XSHIFT, MAIN_WINDOW_YSHIFT = ..., 100

ERROR_WINDOW_XWIDTH, ERROR_WINDOW_YWIDTH = 400, 150
ERROR_WINDOW_XSHIFT, ERROR_WINDOW_YSHIFT = MAIN_WINDOW_XWIDTH // 2, 100 + MAIN_WINDOW_YWIDTH // 2


def resource_path(relative_path):
    """Get absolute path to resource, works for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)


class ErrorWindow(tk.Toplevel):

    def __init__(self, error: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry(f'{ERROR_WINDOW_XWIDTH}x{ERROR_WINDOW_YWIDTH}+'
                      f'{ERROR_WINDOW_XSHIFT + self.winfo_screenwidth() // 5}+{ERROR_WINDOW_YSHIFT}')
        self.resizable(0, 0)
        self.title('Error')

        image_file = resource_path('images\\error.png')
        self.iconphoto(False, tk.PhotoImage(file=image_file))

        t = tk.Text(self, state='normal')

        t.pack()

        t.insert('1.0', error)
        t.config(state='disabled')
