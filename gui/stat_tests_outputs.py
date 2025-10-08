"""File is designed for statistical test outputs (including plots and all what related with them)"""
import tkinter as tk
import tkinter.ttk as ttk
from typing import List
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import statsmodels.api as sm


# HACK: Manually add the project root to sys.path to enable relative imports
# when running 'temporal.py' directly from its location.
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# The linter (e.g., flake8/isort) would normally complain here,
# but the sys.path modification is required for finding 'src'.
from gui.dialogs import ErrorWindow, resource_path  # noqa
import src.gui_backend.functions as funcs  # noqa

plt.style.use('seaborn-v0_8-pastel')


DEFAULT_FONT = 'TkDefaultFont'

AMTIN_WINDOW_XWIDTH, AMTIN_WINDOW_YWIDTH = 900, 600
AMTIN_WINDOW_XSHIFT, AMTIN_WINDOW_YSHIFT = ..., 200  # first parameter is recieved depend on window size

PLOT_VALUES_RESTRICTION = 200  # restriction for number of entries in plots

PLOTS_MATCHER = {
    0: 'Cummulative times plot',
    1: 'Step plot',
    2: 'ACF plots',
}


class AMTOutWindow(tk.Toplevel):

    def __init__(self, parent: tk.Tk, batch_size: int, variables: List[str], plots: List[int], *args, **kwargs):
        """Forms window with AMT test results and its plots

        Args:
            parent (tk.Tk): main TK
            batch_size (int): the size of the batch for batch mean procedure
            variables (List[str]): variables to be used in test
            plots (List[int]): plots to plot
        """
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.variables = variables
        self.plots = plots

        self.geometry(f'{AMTIN_WINDOW_XWIDTH}x{AMTIN_WINDOW_YWIDTH}+'
                      f'{self.winfo_screenwidth() // 4}+{AMTIN_WINDOW_YSHIFT}')
        self.resizable(0, 0)
        self.title('AMT result')

        image_file = resource_path('images\\output_stat_test.png')
        self.iconphoto(False, tk.PhotoImage(file=image_file))

        # scale canvas (and all other) to full size
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SCROLLING IMPLEMENTATION START ---

        scrlbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        scrlbar.grid(row=0, column=1, sticky='NS')

        self.canvas = tk.Canvas(self, yscrollcommand=scrlbar.set)
        self.canvas.grid(row=0, column=0, sticky='NSEW')

        scrlbar.config(command=self.canvas.yview)

        self.content_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor='nw')
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.content_frame.bind('<Configure>', self.__update_scroll_region)
        self.canvas.bind('<Configure>', self.__update_canvas_width)

        # --- MOUSE WHEEL BINDINGS START ---

        # Bind the MouseWheel event to the canvas
        self.canvas.bind('<MouseWheel>', self.__on_mouse_wheel)

        # To make it work across all OSes, you can bind to the content frame too
        # so the wheel works even when the cursor is over the content widgets.
        self.content_frame.bind('<MouseWheel>', self.__on_mouse_wheel)

        # --- LAUNCHING PROCEDURE WORK ---
        done, self.data = funcs.amt(parent.df[self.variables], batch_size)
        if not done:
            ErrorWindow(self.data)
            self.destroy()
            return

        # start results placing
        self.__populate_content()

    def __update_scroll_region(self, event):
        """Updates the scrollable region of the canvas based on content frame size"""
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def __update_canvas_width(self, event):
        """Ensures the content frame stretches to the canvas width"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def __on_mouse_wheel(self, event):
        """Scrolls the canvas when the mouse wheel is used"""

        # Determine the delta (direction and amount of scroll)
        # Windows/macOS event.delta is typically +/- 120 per click
        if sys.platform.startswith('win'):
            # Scroll by the delta, normalized (e.g., divided by 120)
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif sys.platform.startswith('linux'):
            # Linux scroll wheel sends Button-4 (up) or Button-5 (down)
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    def __populate_content(self):
        # All widgets now go into self.content_frame
        for i, (var, res) in enumerate(self.data.items()):
            pvalue_var = tk.StringVar(self.content_frame)
            pvalue_var.set(f'{var} p-value = {res[0]:.2f}')

            # Place p-value label in the content_frame
            entry_pval = tk.Entry(
                self.content_frame,
                font=(DEFAULT_FONT, 10),
                textvariable=pvalue_var,
                state='readonly',  # Makes it read-only but still selectable
                relief='flat',  # Remove the border to look more like a label (optional)
                readonlybackground=self.winfo_toplevel().cget('bg'),  # define parent background to be not highlighted
                cursor="xterm"  # to indicate text in cursor
            )
            entry_pval.grid(row=3 * i + 1, column=0, sticky='W')  # Added sticky='W' for left alignment

            # Place an extra separator for clarity between variables/plots
            ttk.Separator(self.content_frame, orient=tk.HORIZONTAL).grid(
                row=3 * i, column=0, sticky='EW', pady=5
            )

            if self.plots:
                self.__place_plots(3 * i + 2, var)

    def __place_plots(self, i: int, var: str | int):
        # figsize defined experimentally with side ratio 4:3
        # Use self.content_frame as the master for the Matplotlib figure

        if len(self.plots) > 1:
            fig, ax = plt.subplots(len(self.plots), 1, figsize=(8.4, 6), dpi=100)
            scatter = FigureCanvasTkAgg(fig, self.content_frame)

            for n, plot in enumerate(self.plots):
                ax[n].set_title(PLOTS_MATCHER.get(plot, f'Plot {plot} for {var}'), fontsize=8)

                # Set axis labels/properties based on plot type if needed
                match plot:
                    case 0:
                        ax[n].plot(self.parent.df[var][-PLOT_VALUES_RESTRICTION:].cumsum(), label='Cummulative')
                    case 1:
                        ax[n].step(range(len(self.data[var][1][-PLOT_VALUES_RESTRICTION:])),
                                   self.data[var][1][-PLOT_VALUES_RESTRICTION:], label='Step')
                    case 2:
                        sm.graphics.tsa.plot_acf(self.parent.df[var], lags=min(40, len(self.data[var][1]) - 1),
                                                 ax=ax[n], alpha=0.7, c='red')
                        sm.graphics.tsa.plot_acf(self.data[var][1], lags=min(40, len(self.data[var][1]) - 1),
                                                 ax=ax[n], c='blue')
                        ax[n].legend(['original', 'batched'])

                ax[n].tick_params(labelsize=6)
                fig.tight_layout()

            scatter.get_tk_widget().grid(row=i, column=0, padx=5, pady=5, sticky='W')

        # Handling for single plot case
        elif len(self.plots) == 1:
            fig, ax = plt.subplots(figsize=(8.4, 6), dpi=100)
            scatter = FigureCanvasTkAgg(fig, self.content_frame)

            for n, plot in enumerate(self.plots):
                ax.set_title(PLOTS_MATCHER.get(plot, f'Plot {plot} for {var}'), fontsize=8)

                # Set axis labels/properties based on plot type if needed
                match plot:
                    case 0:
                        ax.plot(self.parent.df[var][-PLOT_VALUES_RESTRICTION:].cumsum(), label='Cummulative')
                    case 1:
                        ax.step(range(len(self.data[var][1][-PLOT_VALUES_RESTRICTION:])),
                                self.data[var][1][-PLOT_VALUES_RESTRICTION:], label='Step')
                    case 2:
                        sm.graphics.tsa.plot_acf(self.parent.df[var], lags=min(40, len(self.data[var][1])),
                                                 ax=ax[n], alpha=0.7, c='red')
                        sm.graphics.tsa.plot_acf(self.data[var][1], lags=min(40, len(self.data[var][1])),
                                                 ax=ax[n], c='blue')

                ax.tick_params(labelsize=6)
                fig.tight_layout()
            scatter.get_tk_widget().grid(row=i, column=0, padx=5, pady=5, sticky='W')
