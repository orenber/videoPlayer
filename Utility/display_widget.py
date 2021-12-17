from tkinter import *
from tkinter import ttk
import operator


def center_widget(win:Tk, widget_width:int, widget_height:int)->str:
    #Get the current screen width and height
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    screen_center = (int(screen_width/2), int(screen_height/2))
    widget_center = (int(widget_width/2), int(widget_height/2))
    center_width, center_height = tuple(map(operator.sub, screen_center, widget_center))
    text = "{0}x{1}+{2}+{3}"
    ceter_str = text.format(widget_width,widget_height,center_width,center_height)
    return ceter_str







