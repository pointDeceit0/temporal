""""""
import tkinter as tk


MAIN_WINDOW_XWIDTH, MAIN_WINDOW_YWIDTH = 900, 600
MAIN_WINDOW_XSHIFT, MAIN_WINDOW_YSHIFT = ..., 100

ERROR_WINDOW_XWIDTH, ERROR_WINDOW_YWIDTH = 400, 150
ERROR_WINDOW_XSHIFT, ERROR_WINDOW_YSHIFT = MAIN_WINDOW_XWIDTH // 2, 100 + MAIN_WINDOW_YWIDTH // 2


class ErrorWindow(tk.Toplevel):

    def __init__(self, error: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry(f'{ERROR_WINDOW_XWIDTH}x{ERROR_WINDOW_YWIDTH}+'
                      f'{ERROR_WINDOW_XSHIFT + self.winfo_screenwidth() // 5}+{ERROR_WINDOW_YSHIFT}')
        self.resizable(0, 0)
        self.title('Error')
        self.iconphoto(False, tk.PhotoImage(file=r'.\images\error.png'))

        t = tk.Text(self, state='normal')

        t.pack()

        t.insert('1.0', error)
        t.config(state='disabled')
