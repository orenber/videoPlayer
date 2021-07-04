from tkinter import *
from tkinter import filedialog, ttk, messagebox

root = Tk()
root.title("Image gallery")


panel_main = PanedWindow(bd=4, relief="raised", bg="red")
panel_main.pack(fill=BOTH, expand=1)


label_left = Label(panel_main, text="left Panel")
panel_main.add(label_left)

panel_top = PanedWindow(panel_main, orient=VERTICAL, bd=4, relief="raised",bg="blue")
panel_main.add(panel_top)

label_top = Label(panel_main, text="top")
panel_top.add(label_top)

panel_bottom = PanedWindow(panel_top, orient=VERTICAL, bd=4, relief="raised")
label_bottom = Label(panel_bottom, text="bottom Panel")
panel_bottom.add(label_bottom)
panel_top.add(panel_bottom)

root.mainloop()





