from tkinter import*
import numpy as np
from VideoPlayer import VideoPlayer
from PIL import Image, ImageTk
import os


def extract_image(matrix_image: np.array):

    # apply algo small image

    # convert matrix image to pillow image object
    frame_pillow = Image.fromarray(matrix_image)
    frame_pillow.thumbnail([100, 100])
    # show plat
    photo = ImageTk.PhotoImage(image=frame_pillow)
    # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    board.config(image=photo)
    board.image = photo

    # refresh image display
    board.update()


root = Tk()
root.geometry("700x700+0+0")
titleStr = "demo videoPlayer"
root.title(titleStr)

# main panel
MainPanel = Frame(root, width=500, height=2000, bg="gray24", relief=SUNKEN)
MainPanel.pack(side=TOP)
MainPanel.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

title = Label(MainPanel, font=('arial', 12, 'bold'), text='example how to embedded video player in your application ',
              bg="gray24", fg="snow", bd=10)
title.pack()

txtPlatNumberDisplay = Entry(MainPanel, font=('arial', 20, 'bold'), textvariable='', bd=1, insertwidth=4, bg="black",
                             disabledbackground="black", disabledforeground='snow', justify='center', state='disabled')
txtPlatNumberDisplay.pack(pady=15)

# control panel
control_frame_top = Canvas(MainPanel, width=350, height=5, bg="black", relief=SUNKEN)
control_frame_top.pack(fill=BOTH, expand=False)

board = Label(control_frame_top, width=80, height=-1, bg="black")
board.pack(fill=BOTH, expand=True)

# control panel
control_frame_main = Canvas(MainPanel, width=300, height=700, bg="blue", relief=SUNKEN)
control_frame_main.pack(fill=BOTH, expand=True)

# video player
vid = VideoPlayer(control_frame_main, image=True, algo=True)
vid.command = lambda frame: extract_image(frame)
root.mainloop()
