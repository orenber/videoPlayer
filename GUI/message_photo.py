import tkinter as tk
from tkinter import *
from GUI.dynamic_panel import DynamicPanel


class MessagePhoto(tk.Frame):
    def __init__(self, parent: tk.Tk = None):
        tk.Frame.__init__(self, parent)
        self.build_widget()

    def build_widget(self, root: tk.Tk() = None):

        if root == None:
           self.master.geometry("100x300+800+300")

        # fix window size
        self._main_frame = tk.Frame(root).pack()
        # show to  message
        Label(self._main_frame, text="Label Image ROI:").pack()
        # show image
        matrix = {"row": [{"no_col": [0]}]}
        self._dynamic_panel = DynamicPanel(self._main_frame, matrix)

        T = tk.Text(self._main_frame, height=1, width=10).pack()
        self._button_Cancel = tk.Button(self._main_frame,
                                        text="Cancel",
                                        fg="red",
                                        height=1, width=5,
                                        command=quit).pack(side=tk.RIGHT)
        self._button_Ok = tk.Button(self._main_frame,
                                    text="OK",
                                    height=1,
                                    width=5).pack(side=tk.LEFT)

    def update_image(self, image):
        label_image = self._dynamic_panel.current_label_image
        label_image.config(image=image)


def main():
    message = MessagePhoto()
    message.mainloop()



if __name__ == "__main__":
    main()