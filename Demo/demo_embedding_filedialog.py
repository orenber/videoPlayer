import tkinter.tix as Tix
from tkinter import *


class App:

    def __init__(self, master):
        dirlist = Tix.DirSelectDialog(master,
                                       command=self.showdir)
        frame = Tix.Frame(master)
        frame.pack(fill= BOTH, expand=True)


        dirlist.pack(fill= BOTH, expand=True)

        button = Tix.Button(frame, text="Close",
        command=frame.quit)
        button.pack()

    def showdir(self, directory):

        print("user selected", directory)
        root = Tix.Tk()
        app = App(root)
        root.mainloop()


def main():

    root = Tix.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()