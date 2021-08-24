from tkinter import *
from tkinter import ttk
import numpy as np
from PIL import Image, ImageTk
import cv2


class DynamicPanel(ttk.Frame):

    direction = {"row": VERTICAL, "col": HORIZONTAL}

    def __init__(self, parent=ttk.Frame, matrix: dict = {"row": [{"ncol": [1, 1]}]}):

        ttk.Frame.__init__(self, parent)

        self.key, self.new_cell = list(matrix.items())[0]
        self.main_frame = ttk.Frame
        self.canvas_image = []
        self.label_image = []

        self._canvas_current = Canvas
        self._label_current = Label
        self._label_link = Label
        self._label_frame =  [[0] * 1] * 1
        self._command = []
        self._parent = []
        self._active_parent = PanedWindow
        self._names = dict.fromkeys(list(range(0, len(matrix[self.key]))))

        self._build_widget(parent,matrix)
       #self.current_label_image = self.label_image[0]

    @property
    def names(self):
        return self._names

    @names.setter
    def names(self, names: dict):
        self._names = names

    def set_names(self, names: dict):
        # if the key is not in the list insert new value
        input_list = list(names.keys())
        store_list = list(self._names.keys())
        diff = list(set(input_list) - set(store_list))
        for index in diff:
            self._names[index] = names[index]
        else:
            # if the key is in the list update value
            self._names.update(names)
            for key, name in self._names.items():
                if key < len(self._label_frame):
                    # if the key is in the list update value
                    self._label_frame[key].config(text=name)


    @property
    def command(self):
        return self._command

    @property
    def label_link(self) -> Label:
        return self._label_link

    @command.setter
    def command(self, func):
        # check if the command is lambda expression
        if callable(func):
            self._command = func

    @property
    def current_label_image(self) -> Label:
        return self._label_current

    @property
    def active_parent(self) -> PanedWindow:
        return self._active_parent

    @active_parent.setter
    def active_parent(self, num: int = -1):
        self._active_parent = self._parent[num]

    @label_link.setter
    def label_link(self, widget: Label):
        self._label_link = widget

    @current_label_image.setter
    def current_label_image(self, widget: Label):
        self._label_current = widget
        if callable(self._command):
            self._command()

    @property
    def current_canvas(self) -> Canvas:
        return self._canvas_current

    @current_canvas.setter
    def current_canvas(self, canvas: Canvas):
        self._canvas_current = canvas

    def _build_widget(self, parent=Tk, matrix: dict = {"row": [{"ncol": [1, 1]}]}):

        self.main_frame = ttk.Frame(parent, name ="main_frame_parent")

        self.main_frame.pack( fill=BOTH, expand=1 )

        self._update_widget(self.main_frame, matrix)

    def update_widget(self, matrix: dict = {"row": [{"ncol": [1, 1]}]}):

        self.delete_widget_children(self.main_frame)
        self.reset_parameters()

        self.main_frame.place_forget()
        self.main_frame.destroy()

        self.main_frame = ttk.Frame(self.main_frame.master)
        self.main_frame.pack( fill=BOTH, expand=1 )
        self._update_widget(self.main_frame, matrix)
        pass

    @staticmethod
    def delete_widget_children(parent):
        for child in parent.winfo_children():
            child.destroy()

    def reset_parameters(self):
        self._label_frame = []

    def _update_widget(self, parent, matrix):

        key, new_cell = list(matrix.items())[0]
        signals = list(self.direction.keys())
        if key in signals:
            self.panel_main = PanedWindow(parent, bd=3, relief="raised", bg="gray", orient=self.direction[key])
            self.panel_main.pack(side=TOP, fill=BOTH, expand=1)
            self.parent_panel = self.panel_main

        for index, cell in enumerate(new_cell):
            print(cell)
            key, new_cell = list(cell.items())[0]
            col_num = len(cell[key])

            if key in signals:
                self.la
                self.add_section(key,index)

            else:
                self._parent.append(self.parent_panel)
                self.active_parent = len(self._parent)-1

            for _ in range(0, col_num):
                self.add_cell()

    def add_section(self, key: str = "no_row", index: int = -1 ):

        label = LabelFrame(self.parent_panel)
        self._label_frame.append(label)
        panel = PanedWindow(self._label_frame[index], bd=3, relief="raised", bg="gray", orient=self.direction[key])
        panel.pack(side=TOP, fill=BOTH, expand=1)
        self.parent_panel.add(label, stretch="always")
        self._parent.append(panel)
        self.active_parent = len(self._parent) - 1

    def add_cell(self,index: int =-1):
        self.active_parent = index
        self.canvas_image.append(Canvas(self.active_parent, bg="black", highlightthickness=0))
        self.label_image.append(Label(self.canvas_image[-1], bg="black",
                                      width=44, height=14))
        self.label_image[-1].bind("<Button-1>", self._focus_label)
        self.label_image[-1].pack(fill=BOTH, expand=True, padx=3, pady=3)
        self.canvas_image[-1].pack(fill=BOTH, expand=True)
        self.active_parent.add(self.canvas_image[len(self.canvas_image) - 1], stretch="always")
        self.sct[index].append(index)


    def _focus_label(self, event):
        self.update_default_panel()
        event.widget.config(borderwidth=3, relief="groove")
        self.current_label_image = event.widget
        event.widget.master.config(highlightthickness=3, highlightbackground="yellow")

    def update_default_panel(self):
        [lab.config(relief="flat") for lab in self.label_image]
        [cav.config(highlightthickness=0, highlightbackground="black") for cav in self.canvas_image]
        pass

    def update_image(self, image: np.array, position: int = 0):

        image_pillow = self.matrix_to_pillow(image)
        self.show_image(image_pillow, position)

    def show_image(self, image, position: int = 0):
        # resize image
        image.thumbnail(image.size)
        photo = ImageTk.PhotoImage(image=image)
        # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        board = self.label_image[position]
        board.config(image=photo)
        board.image = photo
        # refresh image display
        board.update()

    @staticmethod
    def matrix_to_pillow(frame: np.array):

        # convert to BGR
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # convert matrix image to pillow image object
        frame_pillow = Image.fromarray(frame_bgr)
        return frame_pillow


def main():

    matrix = {"row": [{"col": [0, 0, 0]}, {"col": [1, 1, 1]}, {"col": [2, 2, 2]}]}
    pan = DynamicPanel(Tk(), matrix)
    pan.set_names({0:"oren"})
    pan.mainloop()

    pass


if __name__ == "__main__":
    main()