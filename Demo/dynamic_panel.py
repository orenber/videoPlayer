

from tkinter import *
from tkinter import filedialog, ttk, messagebox





class DaynamicPanel(ttk.Frame):

    def __init__(self, parent: ttk.Frame = None, **matrix: dict):
        root = Tk()
        root.title( "Image gallery" )


        matrix = {"row": [{"ncol" : [1, 1]}]}


        self.key, self.new_cell = list(matrix.items())[0]



        self._build_widget( parent, self.setup )


    def _build_widget(self, parent: ttk.Frame = None, matrix: dict = dict):

        key, new_cell = list( matrix.items() )[0]
        direction = {"row": VERTICAL, "col": HORIZONTAL}
        signals = list( direction.keys() )

        if key in signals:

            panel_main = PanedWindow(bd=4, relief="raised", bg="red", orient= direction[key])
            panel_main.pack(fill=BOTH, expand=1)
            parent_panel = panel_main

        for cell in new_cell:
            print(cell)
            key, new_cell = list(cell.items())[0]
            col_num = len(cell[key] )
            canvas_image = col_num * [None]
            if key in signals:

                panel = PanedWindow(parent_panel,bd=4, relief="raised", bg="blue", orient= direction[key])
                panel.pack(fill=BOTH, expand=1)
                parent_panel.add(panel)
                parent = panel

            else:
                parent = parent_panel

            for n in range(0, col_num):
                canvas_image[n] = Canvas(parent, bg="black", highlightthickness=1)
                parent.add(canvas_image[n])

root.mainloop()