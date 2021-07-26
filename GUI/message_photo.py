import tkinter as tk
from tkinter import *
from GUI.dynamic_panel import DynamicPanel
from PIL import Image, ImageTk
import cv2
import numpy as np


class MessagePhoto(tk.Frame):
    def __init__(self):
        window = tk.Toplevel()
        tk.Frame.__init__(self, window)
        self.build_widget(window)

    def build_widget(self, root: tk.Tk):

        # fix window size
        self._main_frame = tk.Frame(root).pack()
        # show to  message
        Label(self._main_frame, text="Label Image ROI:").pack()
        # show image
        matrix = {"row": [{"col": [0]}]}
        self._dynamic_panel = DynamicPanel(self._main_frame, matrix)
        self._board = self._dynamic_panel.current_label_image

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

    def update_image(self, image: np.array):

        image_pillow = self.matrix_to_pillow(image)
        self.show_image(image_pillow)

    def show_image(self, image):
        # resize image
        image.thumbnail(image.size)
        photo = ImageTk.PhotoImage(image=image)
        # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        self._board.config(image=photo)
        self._board.image = photo
        # refresh image display
        self._board.update()

    @staticmethod
    def matrix_to_pillow(frame: np.array):

        # convert to BGR
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # convert matrix image to pillow image object
        frame_pillow = Image.fromarray(frame_bgr)
        return frame_pillow







def main():
    message = MessagePhoto()
    message.mainloop()



if __name__ == "__main__":
    main()