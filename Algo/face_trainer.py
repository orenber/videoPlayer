
import pickle

import cv2
import numpy as np
from PIL import Image

from Utility.color_names import COLOR
from Utility.file_location import *
from Utility.logger_setup import setup_logger

try:
    from Algo.detect_mask_video import MaskDetection
except Exception as error:
    print(error)


class FaceTrainer:

    def __init__(self):

        self.log = setup_logger( 'Trainer' )
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.path = os.path.dirname( cv2.__file__ )
        self.face_frontal_path = os.path.join( self.path, 'data', 'haarcascade_frontalface_default.xml' )
        self.face_cascade = cv2.CascadeClassifier( self.face_frontal_path )
        self._path_images = full_file( ["Resources", "images", "faces"] )

        self.set_gray_image = True

        self.face = [{'detect': False, 'pos_label': (None, None), 'ROI': {'x': [None, None], 'y': [None, None]}}]
        self.faces_names = []
        self._last_id = None
        self.current_id = 0
        self.label_ids = {}
        self.ids_label = {}
        self.y_labels = []
        self.x_train = []
        self.label_images = {}
        self.algo_stack = []
        self._id = 0

        self._confident = 45
        self._training = False
        self._image_size = (200, 200)

        try:
            self.mask_detector = MaskDetection()
        except Exception as error:
            self.log.exception(error)

    @property
    def training(self) -> bool:
        return self._training

    @training.setter
    def training(self, train: bool = False):
        self._training = train

    @property
    def confident(self) -> int:
        return self._confident

    @confident.setter
    def confident(self, conf: int = 45) -> None:
        self._confident = conf

    def reset_parameters(self):
        self.current_id = 0
        self.label_ids = {}
        self.y_labels = []
        self.x_train = []
        self.label_images = {}
        self._id = 0
        self.ids_label = {}

    def collect_images(self, images_dir: str):

        self.reset_parameters()
        self._path_images = images_dir

        for root, dirs, files in os.walk( images_dir ):
            for file in files:
                if file.endswith( "png" ) or file.endswith( "jpg" ):
                    path = os.path.join( root, file )
                    label = os.path.basename( os.path.dirname( path ) ).replace( " ", "." ).lower()

                    if label not in self.label_ids:
                        self.ids_label[self.current_id] = label
                        self.label_ids[label] = self.current_id
                        self.current_id += 1
                    self._id = self.label_ids[label]
                    self.label_images[str( self._id )] = []

                    # convert to gray scale
                    pil_image = Image.open( path ).convert( "L" )
                    # resize images to the same size
                    image_resize = pil_image.resize( self._image_size, Image.ANTIALIAS )
                    # convert image to numpy array
                    image_array = np.array( image_resize, "uint8" )

                    self.collect_faces( image_array )

        with open( "labels.pickle", 'wb' ) as f:
            pickle.dump( self.label_ids, f )

        for label, image in zip( self.y_labels, self.x_train ):
            self.label_images[str( label )].append( image )

    def crop_faces(self, image_array):

        faces = self.face_cascade.detectMultiScale( image_array, scaleFactor=1.5, minNeighbors=5 )

        for (x, y, w, h) in faces:
            roi = image_array[y:y + h, x:x + w]
            self.x_train.append( roi )
            self.y_labels.append( self._id )

    def collect_faces(self, face_roi):

        self.x_train.append( face_roi )
        self.y_labels.append( self._id )

    def train_face_detection(self):

        try:
            self.recognizer.train( self.x_train, np.array( self.y_labels ) )
            self.recognizer.save( "trainner.yml" )
        except Exception as error:
            self.log.debug( error )

    def save_roi_faces(self, image: np.array, path: str = ''):

        try:
            # crop the region of interest ( faces in the images)
            folder_unknown = full_file( [self._path_images, 'unknown'] )
            create_folder_if_not_exist( folder_unknown )
            cv2.imwrite( file_date( os.path.join( folder_unknown, "unknown" ), '.png' ), image )

        except Exception as error:
            self.log.debug( error )

    @staticmethod
    def load_labels() -> list:

        with open( "labels.pickle", 'rb' ) as f:
            og_labels = pickle.load( f )
            labels = {v: k for k, v in og_labels.items()}
        return labels

    def face_detection(self, gray_image: np.ndarray, frame_draw:np.ndarray):

        # detect the faces
        faces = self.face_cascade.detectMultiScale( gray_image, 1.1, 4 )
        self.face = [{'detect': False, 'pos_label': (None, None),
                      'ROI': {'x': [None, None], 'y': [None, None]}} for _ in range( len( faces ) )]
        # Draw the rectangle around each face
        for count, (x, y, w, h) in enumerate( faces ):

            if self._training:
                # detect ROI face
                roi = gray_image[y:y + h, x:x + w]
                self.crop_faces( roi )
                self.save_roi_faces( roi )

            self.face[count] = {'detect': True, 'ROI': {'x': (x, x + w), 'y': (y, y + h)},
                                'pos_label': (x + 6, y - 6)}
            cv2.rectangle( frame_draw, (x, y), (x + w, y + h), COLOR['blue'], 2 )
            cv2.putText(frame_draw, 'Face', self.face[count]['pos_label'],
                         cv2.FONT_HERSHEY_DUPLEX, 0.5, COLOR['green'], 1 )

    def face_recognition(self, gray_image: np.ndarray, frame_draw: np.ndarray):

        # detect faces in the image
        faces = self.face_cascade.detectMultiScale( gray_image, scaleFactor=1.5, minNeighbors=5 )
        # go over all the face and plot the rectangle around
        for (x, y, w, h) in faces:

            # detect ROI face
            roi_gray = gray_image[y:y + h, x:x + w]

            # recognizer deep learned model predict keras tensorflow pytorch scikit learn
            id_, conf = self.recognizer.predict(roi_gray)

            if conf >= self._confident:
                name = self.ids_label[id_]

                # take the roi acorrdinet x and y
                points_start = (x, y)
                points_end = (x + w, y + h)
                cv2.putText(frame_draw, name, points_start,
                            cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR['white'], 2, cv2.LINE_AA)
                # draw rectangle around the faces
                cv2.rectangle(frame_draw, points_start, points_end, COLOR['blue'], 2)

    def mask_detection(self, rgb_image: np.ndarray, frame_draw: np.ndarray):

        # detect faces in the frame and determine if they are wearing a
        # face mask or not
        (locs, preds) = self.mask_detector.detect_and_predict_mask(rgb_image)

        # loop over the detected face locations and their corresponding
        # locations
        for (box, pred) in zip(locs, preds):
            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            # determine the class label and color we'll use to draw
            # the bounding box and text
            label = "Mask" if mask > withoutMask else "No Mask"
            color = COLOR["green"] if label == "Mask" else COLOR["red"]

            # include the probability in the label
            label = "{}: {:.2f}%".format( label, max(mask, withoutMask) * 100 )

            # display the label and bounding box rectangle on the output
            # frame
            cv2.putText(frame_draw, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2 )
            cv2.rectangle(frame_draw, (startX, startY), (endX, endY), color, 2)


def main():
    trainer = FaceTrainer()


if __name__ == "__main__":
    main()



