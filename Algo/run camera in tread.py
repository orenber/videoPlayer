
from multiprocessing import Process,Value,Lock

from GUI.Factory import Factory
import cv2


class camThread(Process):


    def __init__(self, previewName, camID):

        Process.__init__(self)

        self.vid = Factory
        self.previewName = previewName
        self.camID = camID



    def run(self):
        print("Starting " + self.previewName)
        #camPreview(self.previewName, self.camID)
        self.vid=Factory()
        self.vid._camera_port = self.camID
        self.vid.mainloop()


def camPreview(previewName, camID):

    cam = cv2.VideoCapture(camID)

    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()

    else:
        rval = False

    while rval:


        rval, frame = cam.read()

        #pan.update_image( frame, 0, 0 )
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)


def main():

    # Create two threads as follows
    thread1 = camThread("Camera 0", 0)
    thread2 = camThread( "Camera 1", 1)
    thread3 = camThread( "Camera 2", 2 )
    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()

if __name__=='__main__':

    main()