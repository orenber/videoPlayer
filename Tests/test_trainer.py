from unittest import TestCase
from GUI.training import Trainer


class TestTrainer(TestCase):

    def setUp(self):
        self.training = Trainer()
        self.training.update()

    def test__init__(self):

        pass


    def test_open_folders(self):

        self.training.open_folders()

        pass

    def test_collect_images(self):
        self.training.collect_images()

        self.fail()

    def test_show_images(self):
        self.fail()

    def test_train_face_detection(self):
        self.fail()

