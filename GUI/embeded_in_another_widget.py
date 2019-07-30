from tkinter import*



root = Tk()



titleStr = "Plate Recognition"
root.title(titleStr)

# main panel
MainPanel = Frame(root, width=500, height=2000, bg="white", relief=SUNKEN)
MainPanel.pack(side=TOP)

title = Label(MainPanel, font=('arial', 12, 'bold'), text='Licence Plate', fg="steel Blue", bd=10)
title.grid(row=0, column=0)
title.pack()
txtPlatNumberDisplay = Entry(MainPanel, font=('arial', 20, 'bold'), textvariable='', bd=30, insertwidth=4,
                         bg="powder blue", justify='right', state=DISABLED)
#txtPlatNumberDisplay.grid(row=1, column=0)
txtPlatNumberDisplay.pack()
# control panel
ControlFrame = Frame(MainPanel, width=350, height=70,bg="orange", relief=SUNKEN)
#ControlFrame.grid(row=2, column=0)
ControlFrame.pack()

#vide = VideoPlayer(ControlFrame)



# control panel
ControlFrame2 = Frame(MainPanel, width=300, height=700,bg="blue", relief=SUNKEN)
#ControlFrame2.grid(row=3, column=0, sticky=N+S+E+W)
ControlFrame2.pack()


vid2e = VideoPlayer(ControlFrame2,camera = True,play=True,image=True)
#vid2e.pack(fill=BOTH, expand=True)
vid2e.mainloop()


