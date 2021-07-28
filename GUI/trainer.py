from GUI.dynamic_panel import DynamicPanel
from tkinter import *
from tkinter import ttk,filedialog
from Utility.file_location import *
import cv2
from PIL import Image
import numpy as np
import pickle


def train_face_detection(x_train: list, y_labels:list):

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(x_train, np.array(y_labels))
    recognizer.save("trainner.yml")

    pass

def collect_images(images_dir:str):

    path = os.path.dirname(cv2.__file__)
    face_frontal_path = os.path.join(path, 'data', 'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(face_frontal_path)

    current_id = 0
    label_ids = {}
    y_labels = []
    x_train = []
    label_images = {}


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
                label_images[str(id_)] = []

                # convert to gray scale
                pil_image = Image.open(path).convert("L")
                # resize images to the same size
                # size = (550, 550)
                # image_resize = pil_image.resize(size, Image.ANTIALIAS)
                # convert image to numpy array
                image_array = np.array(pil_image, "uint8")
                print(image_array)
                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

                for (x, y, w, h) in faces:
                    roi = image_array[y:y + h, x:x + w]
                    x_train.append(roi)
                    y_labels.append(id_)
                    label_images[str(id_)].append(roi)
    with open("labels.pickle", 'wb') as f:
         pickle.dump(label_ids, f)

    train_face_detection(x_train, y_labels)
    return label_images


def open_folders():

    path_image_name = filedialog.askdirectory(title="Select the images folders"
                                              )

    if len(path_image_name) != 0:
        try:
            imagest_dict = collect_images(path_image_name)
            show_images(imagest_dict)
        except Exception as error:
            print("Exception:", error)


def show_images(x_train:list,y_labels:list):

    pass






root = Tk()
root.geometry("500x700+0+0")

icons_path = full_file(["Icons"])
# create Main Frame
main_frame = Frame(root, bg="gray70")
main_frame.pack(fill=BOTH, expand=1)

# control Frame
frame_control = Frame(main_frame, bg="gray70")
frame_control.pack(side=RIGHT, fill=Y, expand=1)


# botton show images
# icon open images folders
icons_open = PhotoImage(file=os.path.join(icons_path, 'folder_open.PNG'))
button_open_images = Button(frame_control,
                            text="Open",
                            image=icons_open,
                            command=lambda :open_folders(),
                            relief='raised')
button_open_images.pack(side=TOP)
button_open_images.config()

# botton train algo
# icon open images folders
icon_train = PhotoImage(file=os.path.join(icons_path, 'ai.PNG'))
button_train = Button(frame_control,
                      text="Train",
                      image=icon_train,
                      command = lambda : train_face_detection())
button_train.pack(side=TOP)


# create canvas
my_canvas = Canvas(main_frame, bg="gray24")
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)


# add scrollbar to the canvas
my_scroll_bar = ttk.Scrollbar(main_frame,
                              orient=VERTICAL,
                              command=my_canvas.yview)
my_scroll_bar.pack(side=RIGHT, fill=Y)

# Configure the canvas
my_canvas.configure(yscrollcommand=my_scroll_bar)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

# create another frame inside the canvas
second_frame = Frame(my_canvas)

# Add that new framne to aWindow in The Canvas
my_canvas.create_window((0,0),window = second_frame,anchor = "nw")
# build open filfe folder button

# build frame images

# build scrollbar

# image gallery
matrix = {"col": [{"row": [0, 0, 0, 0, 0]}
                  ]}
pan = DynamicPanel(second_frame, matrix )

# build to frame control

# build open file folder folder button

root.mainloop()
# sliding bar



