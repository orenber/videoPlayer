from GUI.dynamic_panel import DynamicPanel
from tkinter import *


root =Tk()
root.geometry("500x700+0+0")
# image gallery
matrix = {"row": [{"col": [0, 0, 0,0, 0]},
                  {"col": [1, 1, 1,1,1]},
                  {"col": [2, 2, 2,2,2]},
                  {"col": [3, 3, 3,3,3]},
                  {"col": [4, 4, 4,4,4]},
                  ]}
pan = DynamicPanel(root, matrix )

pan.mainloop()
# sliding bar



