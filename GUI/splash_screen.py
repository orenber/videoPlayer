from tkinter import *
from Utility.file_location import *



class Splash():

    def __init__(self,parent=Tk() ,**kargs):

        self._frame_size =()
        self._title = "AEye Camera"
        self._product_name = "AEye Camera"
        self._icon_image = full_file(["Icons","webcamera.ico"])
        self.splash_root = parent
        self.build_widget()


    def build_widget(self):

        self.splash_root.title(self._title)
        self.splash_root.geometry("300x200+-1500+250")
        self.splash_root.overrideredirect(True)
        self.splash_root.iconbitmap( self._icon_image)

        self.splash_image = PhotoImage( file=os.path.join(full_file(["Icons","surveillance-camera.png"])))
        self.label = Label(self.splash_root,
                           fg="white",
                           font=('arial', 12, 'bold'),
                           bg="white",
                           text=self._product_name,
                           image=self.splash_image)
        self.label.pack(pady=20)

        self.label_poduct_name = Label(self.splash_root,
                                        fg="black",
                                        font=('arial', 18, 'bold'),
                                        bg="white",
                                        text=self._product_name )
        self.label_poduct_name.pack(pady=20)


def main():

    splash = Splash()
    mainloop()

if __name__ == '__main__':
    main()



















