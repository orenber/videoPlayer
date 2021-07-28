from GUI.dynamic_panel import DynamicPanel
from tkinter import *
from tkinter import ttk


root =Tk()
root.geometry("500x700+0+0")

# create Main Frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

# create canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)


# add scrollbar to the canvas
my_scroll_bar = ttk.Scrollbar(main_frame,
                              orient=VERTICAL,
                              command=my_canvas.yview)
my_scroll_bar.pack(side=RIGHT, fill=Y)

# Configure the canvas
my_canvas.configure(yscrollcommand=my_scroll_bar)
my_canvas.bind('<Configure>', lambda e: my_canvas)

# build to frame control

# build open filfe folder button

# build frame images

# build scrollbar

# image gallery
matrix = {"row": [{"col": [0, 0, 0,0, 0]},
                  {"col": [1, 1, 1,1,1]},
                  {"col": [2, 2, 2,2,2]},
                  {"col": [3, 3, 3,3,3]},
                  {"col": [4, 4, 4,4,4]},
                  ]}
pan = DynamicPanel(root, matrix )

# build to frame control

# build open file folder folder button

pan.mainloop()
# sliding bar



