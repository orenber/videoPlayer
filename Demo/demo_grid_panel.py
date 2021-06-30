from tkinter import *
from tkinter import ttk

from tkinter import *
from tkinter import filedialog, ttk, messagebox

root = Tk()
root.title("Image gallery")


panel_main = PanedWindow(bd=4, relief="raised", bg="red", orient=VERTICAL)
panel_main.pack(fill=BOTH, expand=1)
canvas_image = [0,0]


for n in range(0, len(canvas_image)):
    canvas_image[n] = Canvas(panel_main, bg="black", highlightthickness=1)
    panel_main.add(canvas_image[n])

root.mainloop()