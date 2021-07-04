from tkinter import *
from tkinter import ttk

from tkinter import *
from tkinter import filedialog, ttk, messagebox

root = Tk()
root.title("Image gallery")


matrix = {"col": [{"row": [ 1, 1]},{"row": [1, 1, 1]}]}


key, new_cell = list(matrix.items())[0]

direction = {"row": VERTICAL, "col": HORIZONTAL}

if key == "row" or "col":

    panel_main = PanedWindow(bd=4, relief="raised", bg="red", orient= direction[key])
    panel_main.pack(fill=BOTH, expand=1)
    parent_panel = panel_main

for cell in new_cell:
    print(cell)
    key, new_cell = list(cell.items())[0]
    if key == "row" or "col":

        panel = PanedWindow(parent_panel,bd=4, relief="raised", bg="blue", orient= direction[key])
        panel.pack(fill=BOTH, expand=1)
        parent_panel.add(panel)
        parent = panel
        col_num = len(cell[key])
        canvas_image = col_num * [None]

        for n in range(0, col_num):
            canvas_image[n] = Canvas(parent, bg="black", highlightthickness=1)
            parent.add(canvas_image[n])

root.mainloop()