"""File is designed for statistical test outputs (including plots and all what related with them)"""
import tkinter as tk
from typing import List


DEFAULT_FONT = 'TkDefaultFont'

AMTIN_WINDOW_XWIDTH, AMTIN_WINDOW_YWIDTH = 600, 400
AMTIN_WINDOW_XSHIFT, AMTIN_WINDOW_YSHIFT = ..., 100  # first parameter is recieved depend on window size

{
    0: 'Cummulative times plot',
    1: 'Step plot',
    2: 'ACF plots',
}


class AMTOutWindow(tk.Toplevel):

    def __init__(self, parent: tk.Tk, batch_size: int, variables: List[str], plots: List[int], *args, **kwargs):
        super().__init__(*args, **kwargs)
