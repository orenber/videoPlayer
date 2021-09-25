from tkinter import *
from tkinter import ttk
from Utility.file_location import *
from Utility.logger_setup import setup_logger

from GUI.splash_screen import Splash


class AEyeCamera(ttk.Frame):

    def __init__(self, parent: ttk.Frame = None,**kwargs: tuple):
        self.log = setup_logger('AEyeCamera')
        ttk.Frame.__init__(self,parent)
        self._build_widget(parent)

    def _build_widget(self, parent: ttk.Frame = None, **kwargs: tuple):
        self.splash = Splash()
        self.update()
        from GUI.surveillance import Surveillance, Trainer

        self.splash.splash_root.destroy()
        self.log.info("start build widget")
        self.master = Tk()
        self.master.geometry("950x720+0+0")

        # Title bar Title
        self.master.title("SurveillanceCamera")
        # Title Bar Icon
        self.icons_path = full_file( ["Icons","webcamera.ico" ])
        self.master.iconbitmap( self.icons_path)




        self.main_frame = Frame(width=1000,
                                height=720,
                                bg="gray24",
                                relief="raised",
                                name="main_frame")
        self.main_frame.pack(side=TOP)
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.training_frame = Frame( bg="gray24",
                                     relief="raised",
                                     name="training_frame" )
        self.training_frame.pack( side=RIGHT )
        notebook = ttk.Notebook( self.master )
        notebook.pack( fill=BOTH, expand=True )
        notebook.add(self.main_frame, text="Surveillance Camera" )
        self.surveillance = Surveillance( self.main_frame )

        notebook.add(self.training_frame, text="Training")
        self.trainer = Trainer( self.training_frame )



def main():
    a_eye = AEyeCamera()
    a_eye.mainloop()

if __name__ == '__main__':
    main()
