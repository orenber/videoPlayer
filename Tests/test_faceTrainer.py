from unittest import TestCase
from Algo.face_trainer import FaceTrainer
from Utility.file_location import full_file


class TestFaceTrainer(TestCase):

    def setUp(self):
        self.face = FaceTrainer()


    def test_training(self):
        self.assertEqual(self.face.training, False)
        self.face.training = True
        self.assertTrue(self.face.training)

    def test_confident(self):
        self.assertEqual(self.face.confident, 45)
        self.face.confident = 50
        self.assertEqual(self.face.confident, 50)

    def test_reset_parameters(self):
        self.face.reset_parameters()
        self.assertEqual(self.face.y_labels,[])

    def test_collect_images(self):
        folder  = full_file(["Resource","images","Faces","Test"])
        self.face.collect_images(folder)

    def test_crop_faces(self):
        self.fail()

    def test_collect_faces(self):
        self.fail()

    def test_train_face_detection(self):
        self.fail()

    def test_save_roi_faces(self):
        self.fail()

    def test_load_labels(self):
        self.fail()

    def test_face_detection(self):
        self.fail()

    def test_face_recognition(self):
        self.fail()

    def test_mask_detection(self):
        self.fail()
