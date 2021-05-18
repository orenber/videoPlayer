from tkinter import*
from GUI.VideoPlayer import VideoPlayer
import cv2


class Surveillance(VideoPlayer):

    def __init__(self):
        super().__init__(image=True, play=True, camera=True,record = True)

        self.__play = True

    def set_color(self,color:str):

        if color == 'gray':

            color_set = cv2.COLOR_RGB2GRAY
        else:

            color_set = cv2.COLOR_GRAY2RGB

        cv2.cvtColor(frame, color_set)



    def run_frames(self):
        frame_pass = 0

        while self.__cap.isOpened():

            if self.__play:
                # update the frame number
                ret, image_matrix = self.__cap.read()
                # self.frame = image_matrix
                if ret:
                    frame_pass += 1
                    self.update_progress(frame_pass)
                    if self.__record:
                        self.save_frame(image_matrix)

                    # convert matrix image to pillow image object
                    self.frame = self.matrix_to_pillow(image_matrix)
                    self.show_image(self.frame)

                # refresh image display
            self.board.update()

        self.__cap.release()

        cv2.destroyAllWindows()


def main():
    vid = Surveillance()
    vid.mainloop()


if __name__ == "__main__":
    main()