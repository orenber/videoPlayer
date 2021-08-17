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

    def test_set_names(self):
        matrix = self.matrix
        self.test__init__(Tk, matrix)
        self.dyn.set_names({0: "Oren", 2:"Efat"})
        self.dyn.update()

    def test_add_cell(self):
        matrix = self.matrix

        self.test__init__(Tk, matrix)
        self.dyn.active_parent = 0
        self.dyn.add_cell()
        self.dyn.add_cell()
        self.dyn.update()
        self.dyn.add_cell()
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
