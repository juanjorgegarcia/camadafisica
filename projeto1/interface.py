from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import aplicacao
from receiving import *
from postman import *
import os

interface = Tk()

interface.choosed = False

interface.geometry("600x800")

def callback():
    aplicacao.fileName = interface.filename
    aplicacao.main()
    print(interface.filename)

def choosefile():
    
    interface.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    imgSize = StringVar()
    if (interface.choosed == False):
        displayImg()
        interface.choosed = True
        imgSize=(os.stat(interface.filename).st_size)
        global imgInfo, supposedTime
        imgInfo = Label(interface, text=f"Image size: {imgSize} bytes")
        imgInfo.pack(side = "bottom")
        supposedTime = Label(interface, text=f"Supposed transfer time: {round(((imgSize*10)/(115200)),4)} s")
        supposedTime.pack(side = "bottom")
    else:
        updateImg()
        imgSize=(os.stat(interface.filename).st_size) 
        imgInfo.config(text = f"Image size: {imgSize} bytes")
        supposedTime.config(text=f"Supposed transfer time: {round(((imgSize*10)/(115200)),4)} s")
        supposedTime.pack(side = "bottom")
    
    



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
    print(f"ALTURA DA IMAGEM: {()}, LARGURA DA IMAGEM: {interface.img.width()}")

    if (interface.rawImg.getbbox()[2] > interface.rawImg.getbbox()[3]):
        interface.imgThumbnail = ImageTk.PhotoImage(interface.rawImg.resize((400, int(interface.rawImg.getbbox()[3]*400/interface.rawImg.getbbox()[2])),Image.ANTIALIAS))
    else:
        interface.imgThumbnail = ImageTk.PhotoImage(interface.rawImg.resize((int(interface.rawImg.getbbox()[2]*400/interface.rawImg.getbbox()[3]), 400),Image.ANTIALIAS))

    interface.panel.configure(image=interface.imgThumbnail)
    interface.panel.image = interface.imgThumbnail

b2 = Button(interface, text="Choose File", command=choosefile)
b2.pack()


b = Button(interface, text="Send", command=sendInfo)
b.pack(side = "bottom")




interface.mainloop()
