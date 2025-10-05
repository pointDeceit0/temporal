"""File is designed for statistical test inputs (including plots and all what related with them)"""

import tkinter as tk
from typing import Any, List
from stat_tests_outputs import AMTOutWindow


DEFAULT_FONT = 'TkDefaultFont'

AMTIN_WINDOW_XWIDTH, AMTIN_WINDOW_YWIDTH = 600, 400
AMTIN_WINDOW_XSHIFT, AMTIN_WINDOW_YSHIFT = ..., 100  # first parameter is recieved depend on window size


class AMTInWindow(tk.Toplevel):
    # NOTE: initially this window is created only for AMT test, but in future its structure could be redesigned for
    #       more general case. What in thoughts will only affect on names

    def __init__(self, parent: tk.Tk, variables: List[str], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent

        self.geometry(f'{AMTIN_WINDOW_XWIDTH}x{AMTIN_WINDOW_YWIDTH}+'
                      f'{self.winfo_screenwidth() // 4}+{AMTIN_WINDOW_YSHIFT + self.winfo_screenheight() // 5}')
        self.resizable(0, 0)
        self.title('AMT presetting')
        self.iconphoto(False, tk.PhotoImage(file=r'.\images\input_stat_test.png'))

        # stretch column and row for calculate button
        self.grid_rowconfigure(max(len(variables) + 2, 5), weight=1)
        self.grid_columnconfigure(3, weight=1)

        # validation for batch size input
        vcmd = (self.register(self.__validate_input_batch), '%P')

        lbl_batch_size = tk.Label(self, text='Batch size:', font=(DEFAULT_FONT, 10, 'bold'))
        lbl_include_columns = tk.Label(self, text='Columns to include:', font=(DEFAULT_FONT, 10, 'bold'))
        lbl_include_plots = tk.Label(self, text='Plots to include:', font=(DEFAULT_FONT, 10, 'bold'))

        # must be initialized before entry batch size for correct work
        self.btn_calculate = tk.Button(
            self,
            text="Calculate",
            command=self.__on_closing,
            state=tk.DISABLED,
            font=(DEFAULT_FONT, 14, 'normal')
        )

        # Entry for batch size input
        entry_batch_size = tk.Entry(self, font=(DEFAULT_FONT, 10, 'normal'), validate='key', validatecommand=vcmd)
        entry_batch_size.insert(0, 2)

        # grid chechboxes for plots
        self.plots = [[i, tk.IntVar(value=1)] for i, _ in enumerate(range(3))]
        tk.Checkbutton(self, text='Cummulative times plot', variable=self.plots[0][1]).grid(row=2, column=1, sticky='W')
        tk.Checkbutton(self, text='Step plot', variable=self.plots[1][1]).grid(row=3, column=1, sticky='W')
        tk.Checkbutton(self, text='ACF plots', variable=self.plots[2][1]).grid(row=4, column=1, sticky='W')

        # grid variables checkboxes and save theirs results in self.boxes
        self.boxes = []
        for i, v in enumerate(variables):
            var = tk.IntVar(value=1)
            c = tk.Checkbutton(self, text=v, variable=var)
            self.boxes.append([v, var])
            c.grid(row=i + 2, column=0, sticky='W')

        lbl_batch_size.grid(row=0, column=0, sticky='W')
        lbl_include_columns.grid(row=1, column=0)
        lbl_include_plots.grid(row=1, column=1)

        entry_batch_size.grid(row=0, column=1)

        self.btn_calculate.grid(row=max(len(variables) + 2, 5), column=3, sticky=tk.SE)

    def __validate_input_batch(self, v: Any) -> bool:
        """Validate function for batch size input and regulates state of the calculate button depend on it

        Input values may be anything, but only integers will be aplied.

        Args:
            v (Any): tk.Entry input

        Returns:
            bool: validate (True) or not (False)
        """
        if v == '':
            self.btn_calculate.config(state=tk.DISABLED)
            return True
        if v.isdigit():
            self.batch_size = v
            self.btn_calculate.config(state=tk.NORMAL)
            return True
        return False

    def __on_closing(self):
        self.destroy()
        AMTOutWindow(
            self.parent,
            self.batch_size,
            [var for (var, val) in self.boxes if val.get() != 0],
            [num for (num, val) in self.plots if val.get() != 0]
        )
