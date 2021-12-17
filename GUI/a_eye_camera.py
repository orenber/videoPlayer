from tkinter import *
from tkinter import ttk
from Utility.file_location import *
from Utility.logger_setup import setup_logger
from Utility.display_widget import center_widget
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
        self.master.geometry(center_widget(self.master,950,720))

        # Title bar Title
        self.master.title("AEye Camera")
        # Title Bar Icon
        self.icons_path = full_file( ["Icons","webcamera.ico" ])
        self.master.iconbitmap( self.icons_path)
        self.notebook = ttk.Notebook( self.master )
        self.main_frame = Frame(width=1000,
                                height=720,
                                bg="gray24",
                                relief="raised",
                                name="main_frame")

        self.training_frame = Frame(width=1000,
                                     height=720,
                                     bg="gray24",
                                     relief="raised",
                                     name="training_frame" )

        self.surveillance = Surveillance( self.main_frame )
        self.main_frame.pack( fill=BOTH, expand=True )
        self.notebook.add( self.main_frame, text="Surveillance Camera" )
        self.trainer = Trainer( self.training_frame )
        self.training_frame.pack( fill=BOTH, expand=True )
        self.notebook.add( self.training_frame, text="Training" )
        self.notebook.pack(fill=BOTH, expand=True)


def main():
    a_eye = AEyeCamera()
    a_eye.mainloop()

if __name__ == '__main__':
    main()
