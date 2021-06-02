import unittest
from GUI.Surveillance import Surveillance
from time import sleep


class TestSurveillance(unittest.TestCase):

    def test__init__(self):
        self.vid = Surveillance()
        self.vid.update()
        sleep(1)
        pass

    def test_camera_recording(self):
        self.test__init__()
        self.vid.camera_recording()




