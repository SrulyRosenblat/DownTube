from pytube import YouTube
from tkinter import *
from PIL import ImageTk,Image
import threading
import re

YT = YouTube
root= Tk()
RES = StringVar(value='720p')
FORMAT = StringVar(value='mp4')
frame = LabelFrame(root, padx=20,pady=50)

def main():
    frame.pack(padx=0, pady=0)
    box = Entry(frame, width=100 )
    box.insert(0,'enter url:    ')
    box.grid(row=7, column=0, columnspan=4, padx=5, pady=20 )
    t1 =threading.Thread(target=handshake_link, args=[box])
    submit = Button(frame, text='check url',command=lambda:t1.start())
    submit.grid(row=7,column=4)
    
    img = Image.open('gui/shaz.png').resize((300,200))
    test_img = ImageTk.PhotoImage(img)
    pic = Button(frame, image=test_img, command=download_time())
    pic.image = test_img
    pic.grid(row=0,column=2, columnspan =1, rowspan=6) 
     
     
   
    
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
def handshake_link(input_box):
    global YT
    haystack = input_box.get()
    search = "https://www.youtube.com/.*"
    try:
        link = re.search(search, haystack).group()
        print(link)
        YT = YouTube(link) 
        print('linked')  
        
    except:
        print('failed to conect to url')
    clearDisplay(input_box)
    input_box.insert(0,'linking sucsesfull pick your res and click on image to download')
    display_options()
def display_options():
    
    rez = Label(frame,text='Resoulution:')
    rez.grid(row=0,column=3)
    pattern = '\"(\d+)p\"'
    results = re.findall(pattern,str(YT.streams))
    
    results = list(map(int, results))
    results.sort(reverse=True)
    results = [str(result) + 'p' for result in results]
    num = 1
    printed = []
    for resoulution in results:
        if resoulution not in printed:
            x = Radiobutton(frame ,text=resoulution,variable=RES, value=resoulution)
            x.grid(row=num, column= 3)
            num += 1
        printed.append(resoulution) 
        
    download_options = [
        'mp3','mp4'
    ]
    dl = Label(frame, text='download:')
    dl.grid(row=0,column=0)
    num = 1
    for option in download_options:
        x = Radiobutton(frame ,text=option,variable=FORMAT, value=option)
        x.grid(row=num, column= 0)
        num += 1
def download_time():
    print(YT.streams)
def clearDisplay(display):
    display.delete(0, END)



main()
root.mainloop()
# box = Entry(root, width=50)
# box.insert(0,'enter your name')
# box.pack()
# Button(root, text='clickkkkkkkkkkk here!!!!!!!!!!!',command=onClick).pack()
