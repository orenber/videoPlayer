from unittest import TestCase


from GUI.dynamic_panel import DynamicPanel
from tkinter import *
import numpy as np
from PIL import Image, ImageTk
import os


class TestDynamicPanel(TestCase):

    def setUp(self) -> None:
        self.matrix = {"row": [{"col": [0, 0, 0]}, {"col": [1, 1, 1]}, {"col": [2, 2, 2]}]}
        return

    def test__init__(self, tk=Tk, matrix: dict = {"row": [{"col": [0, 0, 0]}, {"col": [1, 1, 1]}, {"col": [2, 2, 2]}]}):
        self.dyn = DynamicPanel(tk(), matrix)
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


    def test_current_canvas(self):
        self.fail()

    def test_current_canvas(self):
        self.fail()

    def test__build_widget(self):
        self.fail()

    def test_update_widget(self):

        matrix = {"row": [{"col": [0, 0, 0]}, {"row": [2, 2, 2,3]}]}

        self.test__init__(Tk, matrix)
        self.dyn.update()
        self.dyn.update_widget(self.matrix)
        self.dyn.update()

    def test_names_1(self):
        matrix = self.matrix
        self.test__init__(Tk, matrix)
        self.dyn.names = {0: "Oren", 1: "Hadass", 2: "Leora"}
        names = self.dyn.names
        print(names)
        self.assertDictEqual(names,self.dyn.names, "dictionary is not the same")

    def test_names_2(self):
        matrix = self.matrix
        self.test__init__(Tk, matrix)
        self.dyn.names = {0: "Oren", 1: "Hadass", 2: "Leora"}
        self.dyn.set_names({0: "Oren", 1: "Efat", 3: "Amir"})
        names = self.dyn.names
        self.assertDictEqual(names, self.dyn.names, "dictionary is not the same")
        print(names)

    def test_set_names(self):

        self.test__init__(Tk, self.matrix)
        self.dyn.set_names({0: "Oren", 2: "Efat"})
        names = self.dyn.names
        self.assertDictEqual( names, self.dyn.names, "dictionary is not the same" )
        self.dyn.update()

    def test_add_cell(self):

        self.test__init__(Tk, self.matrix)
        self.dyn.add_cell(0)
        self.dyn.add_cell(2)

        self.dyn.update()


    def test__focus_label(self):
        self.fail()

    def test_update_default_panel(self):
        self.fail()

    def test_update_image(self):
        self.test__init__( Tk, self.matrix )

        # load image
        images_path = os.path.abspath(os.path.join( os.pardir, 'Resources', 'images' ) )
        image_file = os.path.join(images_path, '301-F.jpg' )
        image_pillow = Image.open(image_file )
        image_test = np.array(image_pillow)

        self.dyn.update_image(image_test,1,1)
        self.dyn.update()
        pass

    def test_show_image(self):
        self.test__init__(Tk, self.matrix )

        # load image
        images_path = os.path.abspath(os.path.join( os.pardir, 'Resources', 'images'))
        image_file = os.path.join(images_path, '301-F.jpg')
        self.image_test = Image.open(image_file)

        self.dyn.show_image(self.image_test, 1, 1)
        self.dyn.update()

    def test_matrix_to_pillow(self):
        self.fail()

    def test_add_section(self):
        matrix = self.matrix

        self.test__init__(Tk, matrix)
        self.dyn.add_section('row', 3)
        self.dyn.add_section('col', 4)
        self.dyn.add_cell(3)
        self.dyn.add_cell(0)
        self.dyn.add_cell(4)
        self.dyn.add_cell(4)

