import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from Utility import file_location
from GUI.dynamic_panel import DynamicPanel

root = tk.Tk()
root.geometry("100x300+800+300")
# fix window size
main_frame = tk.Frame(root).pack()
# show to  messege
Label(main_frame, text="Label Image ROI:").pack()
# show image
matrix = {"row": [{"no_col": [0]}]}
pan = DynamicPanel(main_frame, matrix )

T = tk.Text(main_frame, height=1, width=10).pack()
button_Cancel = tk.Button(main_frame,
                   text="Cancel",
                   fg="red",
                   height=1, width=5,
                   command=quit).pack(side=tk.RIGHT)
button_Ok = tk.Button(main_frame, text="OK",  height=1, width=5,).pack(side=tk.LEFT)

root.mainloop()