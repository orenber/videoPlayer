from tkinter import *
from tkinter import ttk


class DynamicPanel(ttk.Frame):

    direction = {"row": VERTICAL, "col": HORIZONTAL}

    def __init__(self, parent=ttk.Frame, matrix: dict = {"row": [{"ncol": [1, 1]}]}):

        ttk.Frame.__init__(self, parent)

        self.key, self.new_cell = list(matrix.items())[0]

        self.canvas_image = []

        self._build_widget(parent, matrix)

    def _build_widget(self, parent=Tk, matrix: dict = {"row": [{"ncol": [1, 1]}]}):

        key, new_cell = list(matrix.items())[0]

        signals = list(self.direction.keys())

        if key in signals:

            self.panel_main = PanedWindow(parent, bd=1, relief="raised", bg="red", orient=self.direction[key])
            self.panel_main.pack(fill=BOTH, expand=1)
            parent_panel = self.panel_main

        for cell in new_cell:
            print(cell)
            key, new_cell = list(cell.items())[0]
            col_num = len(cell[key])

            if key in signals:

                panel = PanedWindow(parent_panel, bd=1, relief="raised", bg="blue", orient=self.direction[key])
                panel.pack(fill=BOTH, expand=1)
                parent_panel.add(panel, stretch="always")
                parent = panel

            else:
                parent = parent_panel

            for _ in range(0, col_num):
                self.canvas_image.append(Canvas(parent, bg="black", highlightthickness=0))
                self.canvas_image[-1].bind("<Button-1>", self._focus)
                parent.add(self.canvas_image[len(self.canvas_image)-1], stretch="always")

    def _focus(self, event):

        self.update_defult_canvas()

        event.widget.config(highlightthickness=3, highlightbackground="yellow")

        pass

    def update_defult_canvas(self):
        [can.config(highlightthickness=0, highlightbackground="black") for can in self.canvas_image]
        pass


def main():

    matrix = {"col": [{"row": [0, 0, 0]}, {"row": [1, 1, 1]}, {"row": [2, 2, 2]}]}
    pan = DynamicPanel(Tk(), matrix)
    pan.canvas_image
    pan.mainloop()

    pass


if __name__ == "__main__":
    main()