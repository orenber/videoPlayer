from tkinter import*
import numpy as np
from GUI.videoPlayer import VideoPlayer
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
MainPanel = Frame(root, width=1500, height=2000, bg="gray24", relief="raised")
MainPanel.pack(side=TOP)
MainPanel.place(relx=0, rely=0, relwidth=1, relheight=1)

title = Label(MainPanel, font=('arial', 12, 'bold'), text='Demo: how to reparent video player widget in your application',
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

# video player
vid = VideoPlayer(control_frame_main, image=True, algo=True)
vid.command = lambda frame: extract_image(frame)
root.mainloop()
