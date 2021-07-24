import os
import cv2
import numpy as np
from Utility.file_location import *
from PIL import Image
import pickle

images_dir = full_file([os.pardir, "Resources", "images"])
face_frontal_path = os.path.join(images_dir, 'data', 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(face_frontal_path)
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
y_labels = []
x_train = []

print(images_dir)

for root, dirs, files in os.walk(images_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(os.path.dirname(path)).replace(" ", ".").lower()
            print(label, path)

            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]
            print(label_ids)

            # convert to gray scale
            pil_image = Image.open(path).convert("L")
            # resize images to the same size
            size = (550, 550)
            image_resize = pil_image.resize(size, Image.ANTIALIAS)
            # convert image to numpy array
            image_array = np.array(image_resize, "uint8")
            print(image_array)
            faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

            for (x, y, w, h) in faces:

                roi = image_array[y:y+h, x:x+w]
                x_train.append(roi)
                y_labels.append(id_)
with open("labels.pickle", 'wb') as f:
    pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainner.yml")











