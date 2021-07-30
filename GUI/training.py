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
        self._frame_control = Frame(self._main_frame, bg="gray70",width=100)
        self._frame_control.pack(side=RIGHT, fill=Y, expand=0)

        self._frame_control_x = Frame( self._main_frame, bg="gray70")
        self._frame_control_x.pack( side=BOTTOM, fill=X, expand=0 )

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
        button_train_tooltip.bind(self._button_train, "Training data" )

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
        self._scroll_bar_x = ttk.Scrollbar(self._frame_control_x,
                                            orient=HORIZONTAL,
                                            command=self._canvas.xview)
        self._scroll_bar_x.pack(side=TOP, fill=X,expand=0)
        scroll_bar_x_tooltip = Pmw.Balloon(self._frame_control_x)
        scroll_bar_x_tooltip.bind( self._scroll_bar_x, "Scroll images in x direction" )

        # Configure the canvas
        self._canvas.configure(yscrollcommand=self._scroll_bar_y, xscrollcommand=self._scroll_bar_x)
        self._canvas.bind('<Configure>', lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))

        # create another frame inside the canvas
        self._frame_display = Frame(self._canvas)
        # image gallery
        matrix = {"col": [{"row": [0, 0, 0, 0, 0, 0, 0, 0, 0,0]},
                          {"row": [0, 0, 0, 0, 0, 0, 0, 0, 0,0]}
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

        d = 10
        n = 1
        for label, images in label_images.items():

            if len(label_images[label]) > 0:

                index = d*(n-1)
                n += 1
                for image in images:
                    self._image_gallery.update_image(image, index)
                    index += 1

    def open_folders(self):

        path_image_name = filedialog.askdirectory(title="Select the images folders")

        if len( path_image_name ) != 0:
            try:
                self.collect_images(path_image_name)
                self.show_images(self.label_images)
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

                    self.collect_faces(image_array)

        with open("labels.pickle", 'wb') as f:
            pickle.dump(self.label_ids, f)
        
        for label, image in zip(self.y_labels,self.x_train):
            self.label_images[str(label)].append(image)

    def crop_faces(self,image_array):

        faces = self.face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5 )

        for (x, y, w, h) in faces:
            roi = image_array[y:y + h, x:x + w]
            self.x_train.append(roi)
            self.y_labels.append(self.id_)

    def collect_faces(self,face_roi):

        self.x_train.append(face_roi)
        self.y_labels.append(self.id_)

    def train_face_detection(self):

        self.recognizer.train(self.x_train, np.array( self.y_labels))
        self.recognizer.save("trainner.yml" )

        pass

    def face_recognition(self):

        # segment cv2 path

        labels = {"person_name": 1}
        font = cv2.FONT_HERSHEY_SIMPLEX
        stroke = 2
        color = (255, 255, 255)

        with open( "labels.pickle", 'rb' ) as f:
            og_labels = pickle.load( f )
            labels = {v: k for k, v in og_labels.items()}

        cap = cv2.VideoCapture(0)

        while (True):

            # capture frame by frame
            ret, frame = cap.read()
            # convert BGR image to gray
            gray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY )
            # detect faces in the image
            faces = self.face_cascade.detectMultiScale( gray, scaleFactor=1.5, minNeighbors=5 )
            # go over all the face and plot the rectangle around
            for (x, y, w, h) in faces:

                # detect ROI face
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]

                # recognizer deep learned model predict keras tensorflow pytorch scikit learn
                id_, conf = self.recognizer.predict(roi_gray)

                if conf >= 47:
                    name = labels[id_]
                    cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, stroke, cv2.LINE_AA )

                    # crop the region of intrest ( faces in the images)
                    # cv2.imwrite(file_date(images_face_path, '.png'), roi_gray)
                    # take the roi corrdinet x and y
                    points_start = (x, y)
                    points_end = (x + w, y + h)
                    # draw rectangle around the faces
                    cv2.rectangle( frame, points_start, points_end, (255, 0, 0), 3 )

            # display image and plot
            cv2.imshow( 'frame', frame )
            # press quite to Exit the loop
            if cv2.waitKey( 20 ) & 0xFF == ord( 'q' ):
                break

        # when everything done , realse the capture

        cap.release()
        cv2.destroyAllWindows()


def main():
    trainer = Trainer()
    trainer.mainloop()


if __name__ == "__main__":
    main()



