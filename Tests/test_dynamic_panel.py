from unittest import TestCase
from GUI.dynamic_panel import DynamicPanel
from tkinter import *


class TestDynamicPanel(TestCase):

    def setUp(self) -> None:
        self.matrix = {"col": [{"col": [0, 0, 0]}, {"col": [1, 1, 1]}, {"col": [2, 2, 2]}]}
        return

    def test__init__(self, tk, matrix):
        self.dyn = DynamicPanel(Tk(), matrix)
        self.assertIsInstance(self.dyn, DynamicPanel, "this is not DynamicPanel instance")

    def test_command(self):
        self.fail()

    def test_command(self):
        self.fail()

    def test_label_link(self):
        self.fail()

    def test_label_link(self):
        self.fail()

    def test_current_label_image(self):
        self.fail()

    def test_current_label_image(self):
        self.fail()

    def test_active_parent(self):
        self.test__init__()
        self.dyn.active_parent

    def test_active_parent(self):
        self.fail()

    def test_current_canvas(self):
        self.fail()

    def test_current_canvas(self):
        self.fail()

    def test__build_widget(self):
        self.fail()

    def test_names(self):
        matrix = self.matrix
        self.test__init__(Tk, matrix)
        self.dyn.names = {0: "Oren", 1: "Hadass", 2: "Leora"}
        names = self.dyn.names
        print(names)
        self.dyn.mainloop()
        self.assertDictEqual(names,self.dyn.names, "dictionary is not the same")

    def test_names(self):
        matrix = self.matrix
        self.test__init__(Tk, matrix)
        self.dyn.names = {0: "Oren", 1: "Hadass", 2: "Leora"}
        self.dyn.set_names({0: "Oren", 1: "Efat", 3: "Amir"})
        names = self.dyn.names
        print(names)

        self.dyn.update()

    def test_set_names(self):
        matrix = self.matrix
        self.test__init__(Tk, matrix)
        self.dyn.set_names({0: "Oren", 1: "Efat"})
        self.dyn.update()

    def test_add_cell(self):
        matrix = self.matrix

        self.test__init__(Tk, matrix)
        self.dyn.add_cell(0)
        self.dyn.add_cell(2)
        self.dyn.update()
        self.dyn.add_cell(1)
        self.dyn.update()

    def test__focus_label(self):
        self.fail()

    def test_update_default_panel(self):
        self.fail()

    def test_update_image(self):
        self.fail()

    def test_show_image(self):
        self.fail()

    def test_matrix_to_pillow(self):
        self.fail()

    def test_add_section(self):
        matrix = self.matrix

        self.test__init__(Tk, matrix)
        self.dyn.add_section('row',{3: 'Amir'})
        self.dyn.update()
        self.dyn.mainloop()
