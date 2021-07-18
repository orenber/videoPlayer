from tkinter import*
import numpy as np
from GUI.dynamic_panel import DynamicPanel
from PIL import Image, ImageTk


root = Tk()

root.geometry("700x700+0+0")
titleStr = "demo DynamicPanel"
root.title(titleStr)

# main panel
MainPanel = Frame(root, width=1500, height=2000, bg="gray24", relief="raised")
MainPanel.pack(side=TOP)
MainPanel.place(relx=0, rely=0, relwidth=1, relheight=1)

title = Label(MainPanel, font=('arial', 12, 'bold'),
              text='Demo: how to re parent DynamicPanel widget in your application',
              bg="gray24", fg="snow", bd=10)
title.pack()

txtPlatNumberDisplay = Entry(MainPanel, font=('arial', 20, 'bold'), textvariable='', bd=1, insertwidth=4, bg="black",
                             disabledbackground="black", disabledforeground='snow', justify='center', state='disabled')
txtPlatNumberDisplay.pack(pady=15)

# control panel
control_frame_top = Canvas(MainPanel, width=900, height=5, bg="black", relief="raised")
control_frame_top.pack(fill=BOTH, expand=True)

board = Label(control_frame_top, width=600, height=-1, bg="black")
board.pack(fill=BOTH, expand=True)

# control panel
control_frame_main = Canvas(MainPanel, width=600, height=700, bg="blue", relief="raised")
control_frame_main.pack(fill=BOTH, expand=True)

# Dynamic Panel
matrix = {"col": [{"row": [0, 0, 0]}, {"norow": [1]}]}
pan = DynamicPanel(control_frame_main, matrix)
pan.canvas_image
pan.mainloop()

