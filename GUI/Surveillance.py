from tkinter import*
from GUI.VideoPlayer import VideoPlayer
import cv2


class Surveillance(VideoPlayer):

    def __init__(self):
        super().__init__(image=True, play=True, camera=True,record = True)

        self.__play = True






def main():
    vid = Surveillance()
    vid.mainloop()


if __name__ == "__main__":
    main()