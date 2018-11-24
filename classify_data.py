# Simple enough, just import everything from tkinter.
from tkinter import *
import pathlib
import pickle


#download and install pillow:
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow
from PIL import Image, ImageTk

# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master
        self._tested_arr_path = 'tested_arr.pkl'

        #with that, we want to then run init_window, which doesn't yet exist
        
        self.p = pathlib.Path('./data')
        try:
            with open(self._tested_arr_path, 'rb') as f:
                self.tested_arr = pickle.load(f)
        except FileNotFoundError:
            self.tested_arr = []
        self.generator = self.next_path()
        self.current_img = next(self.generator)
        print("First img", self.current_img)
        while self.current_img in self.tested_arr:
            self.current_img = next(self.generator)
        self.init_window()

    def next_path(self):
        for i in self.p.iterdir():
            if '.' not in str(i):
                for image_path in i.iterdir():
                    yield str(image_path)

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("Classify Cloud data yourself!")
        self.master.bind("a", self.move_image)
        self.master.bind("d", self.delete_image)
        self.master.bind("z", self.undo_action)
        self.master.bind("<Return>", self.next_image)
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)
        
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Exit", command=self.client_exit)

        #added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        # create the file object)
        edit = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        #edit.add_command(label="Show Img", command=self.showImg)
        #edit.add_command(label="Show Text", command=self.showText)


        #added "file" to our menu
        menu.add_cascade(label="Edit", menu=edit)
        self.showImg()

    def showImg(self):
        load = Image.open(self.current_img)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        self.img = Label(self, image=render)
        self.img.image = render
        self.img.place(x=0, y=0)
    

    def move_image(self, event=None):
        no_cloud_path = pathlib.Path('./data/no_clouds/')
        source = pathlib.Path(self.current_img)
        destination = no_cloud_path / (str(len(self.tested_arr)) + source.suffix)
        with destination.open(mode='xb') as fid:
            fid.write(source.read_bytes())
            source.unlink()
        print("Image moved to", str(destination))

    def  delete_image(self, event=None):
        source = pathlib.Path(self.current_img)
        source.unlink()
        print("image deleted!")
    
    def next_image(self, event=None):
        self.tested_arr.append(
            self.current_img
        )
        try:
            self.current_img = next(self.generator)
        except StopIteration:
            print("NO MORE IMAGES!")
            return
        print("next img", self.current_img)
        load = Image.open(self.current_img)
        render = ImageTk.PhotoImage(load)
        self.img.configure(image=render)
        self.img.image = render

    def undo_action(self):
        pass



    def showText(self):
        text = Label(self, text="Hey there good lookin!")
        text.pack()
        

    def client_exit(self):
        exit()


# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()

root.geometry("600x600")

#creation of an instance
app = Window(root)


#mainloop 
root.mainloop()  