from unittest import TestCase
from GUI.Surveillance import Surveillance


class TestSurveillance(TestCase):

    def test__init__(self):
        self.vid = Surveillance()
        self.vid.update()
        pass

    def test_algo_list(self):
        self.fail()

    def test_run_frames(self):
        self.fail()

    def test_movement_detection(self):
        self.fail()

    def test_face_detection(self):
        self.fail()

    def test_profile_detection(self):
        self.fail()

    def test_record_movement(self):
        self.fail()

    def test_save_frame(self):
        self.fail()
