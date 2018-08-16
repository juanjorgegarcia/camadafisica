from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import aplicacao



interface = Tk()

interface.choosed = False

interface.geometry("600x800")

def callback():
    aplicacao.fileName = interface.filename
    aplicacao.main()
    print(interface.filename)

def choosefile():
    interface.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    if (interface.choosed == False):
        displayImg()
        interface.choosed = True
    else:
        updateImg()

def displayImg():
    interface.rawImg = Image.open(interface.filename)

    # if (interface.choosed):
    #     interface.panel.destroy()

    #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    interface.img = ImageTk.PhotoImage(interface.rawImg)

    if (interface.rawImg.getbbox()[2] > interface.rawImg.getbbox()[3]):
        interface.imgThumbnail = ImageTk.PhotoImage(interface.rawImg.resize((400, int(interface.rawImg.getbbox()[3]*400/interface.rawImg.getbbox()[2])),Image.ANTIALIAS))
    else:
        interface.imgThumbnail = ImageTk.PhotoImage(interface.rawImg.resize((int(interface.rawImg.getbbox()[2]*400/interface.rawImg.getbbox()[3]), 400),Image.ANTIALIAS))

    #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    interface.panel = Label(interface, image = interface.imgThumbnail)

    #The Pack geometry manager packs widgets in rows or columns.
    interface.panel.pack(side = "bottom", fill = "both", expand = "yes")

def updateImg():
    interface.rawImg = Image.open(interface.filename)

    interface.img = ImageTk.PhotoImage(interface.rawImg)

    if (interface.rawImg.getbbox()[2] > interface.rawImg.getbbox()[3]):
        interface.imgThumbnail = ImageTk.PhotoImage(interface.rawImg.resize((400, int(interface.rawImg.getbbox()[3]*400/interface.rawImg.getbbox()[2])),Image.ANTIALIAS))
    else:
        interface.imgThumbnail = ImageTk.PhotoImage(interface.rawImg.resize((int(interface.rawImg.getbbox()[2]*400/interface.rawImg.getbbox()[3]), 400),Image.ANTIALIAS))

    interface.panel.configure(image=interface.imgThumbnail)
    interface.panel.image = interface.imgThumbnail

b2 = Button(interface, text="Choose File", command=choosefile)
b2.pack()

b = Button(interface, text="Send", command=callback)
b.pack(side = "bottom")


interface.mainloop()
