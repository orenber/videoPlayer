from GUI.dynamic_panel import DynamicPanel
from tkinter import *
from tkinter import ttk, filedialog
from Utility.file_location import *
import cv2
from PIL import Image
import numpy as np
import pickle
import Pmw


class Trainer(ttk.Frame):

    def __init__(self, parent: ttk.Frame = None):

        ttk.Frame.__init__( self, parent)

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.path = os.path.dirname(cv2.__file__)
        self.face_frontal_path = os.path.join(self.path, 'data', 'haarcascade_frontalface_default.xml' )
        self.face_cascade = cv2.CascadeClassifier(self.face_frontal_path)

        self.current_id = 0
        self.label_ids = {}
        self.y_labels = []
        self.x_train = []
        self.label_images = {}
        self.build_widget()

    def build_widget(self, parent: ttk.Frame = None):

        if parent == None:

            self.master.geometry("470x700+0+0")
        else:
            self.master = parent
            Pmw.initialize(self.master)

        self._icons_path = full_file(["Icons"])

        # create Main Frame
        self._main_frame = Frame(self.master, bg="gray70")
        self._main_frame.pack(fill=BOTH, expand=1)

        # control Frame
        self._frame_control = Frame(self._main_frame, bg="gray70")
        self._frame_control.pack(side=RIGHT, fill=Y, expand=1)


        # botton show images
        # icon open images folders
        self._icons_open = PhotoImage(file=os.path.join(self._icons_path, 'folder_open.PNG'))
        self._button_open_images = Button(self._frame_control,
                                          text="Open",
                                          image=self._icons_open,
                                          command=lambda: self.open_folders(),
                                          relief='raised')
        self._button_open_images.pack(side=TOP)
        button_open_tooltip = Pmw.Balloon(self._frame_control)
        button_open_tooltip.bind(self._button_open_images, "Open images main folders")

        # botton train algo
        # icon open images folders
        self._icon_train = PhotoImage(file=os.path.join(self._icons_path, 'ai.PNG'))
        self._button_train = Button(self._frame_control,
                                    text="Train",
                                    image=self._icon_train,
                                    command=lambda: self.train_face_detection())
        self._button_train.pack(side=TOP)
        button_train_tooltip = Pmw.Balloon( self._frame_control)
        button_train_tooltip.bind( self._button_train, "Training data" )

        # create canvas
        self._canvas = Canvas(self._main_frame, bg="gray24")
        self._canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # add scrollbar to the canvas
        self._scroll_bar_y = ttk.Scrollbar(self._main_frame,
                                           orient=VERTICAL,
                                           command=self._canvas.yview)
        self._scroll_bar_y.pack(side=RIGHT, fill=Y)
        scroll_bar_y_tooltip = Pmw.Balloon(self._frame_control)
        scroll_bar_y_tooltip.bind(self._scroll_bar_y, "Scroll images in y direction")

        # add scrollbar in the x direction
        self._scroll_bar_x = ttk.Scrollbar( self._main_frame,
                                            orient=HORIZONTAL,
                                            command=self._canvas.xview)
        self._scroll_bar_x.pack(side=TOP, fill=X)
        scroll_bar_x_tooltip = Pmw.Balloon( self._frame_control )
        scroll_bar_x_tooltip.bind( self._scroll_bar_x, "Scroll images in x direction" )

        # Configure the canvas
        self._canvas.configure(yscrollcommand=self._scroll_bar_y, xscrollcommand=self._scroll_bar_x)
        self._canvas.bind('<Configure>', lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))

        # create another frame inside the canvas
        self._frame_display = Frame(self._canvas)
        # image gallery
        matrix = {"col": [{"row": [0, 0, 0, 0, 0]},
                          {"row": [0, 0, 0, 0, 0]}
                          ]}

        self._image_gallery = DynamicPanel(self._frame_display, matrix)
        # Add that new frame to aWindow in The Canvas
        self._canvas.create_window((0, 0), window=self._frame_display, anchor="nw")
        # build open file folder button

        # build frame images

        # build scrollbar

        # build to frame control

        # build open file folder folder button

        # sliding bar

    def show_images(self, label_images: dict):
        pass

    def open_folders(self):

        path_image_name = filedialog.askdirectory(title="Select the images folders"
                                                   )

        if len( path_image_name ) != 0:
            try:
                self.collect_images(path_image_name)
                self.show_images(self.imagest_dict)
            except Exception as error:
                print("Exception:", error )

    def collect_images(self,images_dir: str):

        for root, dirs, files in os.walk( images_dir ):
            for file in files:
                if file.endswith("png") or file.endswith("jpg"):
                    path = os.path.join(root, file)
                    label = os.path.basename(os.path.dirname(path)).replace( " ", ".").lower()
                    print(label, path)

                    if not label in self.label_ids:
                        self.label_ids[label] = self.current_id
                        self.current_id += 1
                    self.id_ = self.label_ids[label]
                    self.label_images[str(self.id_)] = []

                    # convert to gray scale
                    pil_image = Image.open(path).convert( "L" )
                    # resize images to the same size
                    # size = (550, 550)
                    # image_resize = pil_image.resize(size, Image.ANTIALIAS)
                    # convert image to numpy array
                    image_array = np.array( pil_image, "uint8" )
                    print(image_array)
                    faces = self.face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

                    for (x, y, w, h) in faces:
                        roi = image_array[y:y + h, x:x + w]
                        self.x_train.append(roi )
                        self.y_labels.append(self.id_)
                        self.label_images[str(self.id_)].append(roi)
        with open("labels.pickle", 'wb') as f:
            pickle.dump(self.label_ids, f)

    def train_face_detection(self,x_train: list, y_labels: list):

        self.recognizer.train( x_train, np.array( y_labels ) )
        self.recognizer.save( "trainner.yml" )

        pass


def main():
    trainer = Trainer()
    trainer.mainloop()


if __name__ == "__main__":
    main()



