from pytube import YouTube
from tkinter import *
from PIL import ImageTk,Image


def main():
    print('hi')
    frame = LabelFrame(root, padx=20,pady=50)
    frame.pack(padx=0, pady=0)
    box = Entry(frame, width=100 )
    box.insert(0,'enter url:    ')
    box.grid(row=2, column=0, columnspan=4, padx=5, pady=20 )
    submit = Button(frame, text='check url',command=onClick)
    submit.grid(row=2,column=4)
    
    img = Image.open('gui/shaz.png').resize((300,200))
    print(img.size)
    # returns <class 'PIL.PngImagePlugin.PngImageFile'>
    print(type(img))
    test_img = ImageTk.PhotoImage(img)
    #returns <class 'PIL.ImageTk.PhotoImage'>
    print(type(test_img))
    pic = Button(frame, image=test_img)
    pic.image = test_img
    pic.grid(row=0,column=2, columnspan =1) 
     
    #.grid(row=1, column=1, columnspan=2)
    # link = input('enter a url to download:  ')
    # try:
    #     yt = YouTube(link)   
    # except:
    #     print('failed to conect to url')

    # choice = input('enter the resoulution:  ')
    # while True:
    #     vid = yt.streams.filter(res = choice,  progressive = True ).first()
    #     if not vid:
    #         vid = yt.streams.filter(res = choice + 'p',  progressive = True ).first()
    #     if vid:
    #         break
    #     choice = input('resoulution unavailable enter again:  ')
    # print('downloading..')
    # vid.download(r'C:\Users\sruls\OneDrive\Desktop\yt-dl', yt.title)

    # print('download complete of "' + yt.title + '"')
    
def onClick():
    hello ='hello ' + box.get()
    #Label(root, text=hello).pack()
root= Tk()
main()
# box = Entry(root, width=50)
# box.insert(0,'enter your name')
# box.pack()
# Button(root, text='clickkkkkkkkkkk here!!!!!!!!!!!',command=onClick).pack()
root.mainloop()