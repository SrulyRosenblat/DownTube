from pytube import YouTube
from tkinter import *
from PIL import ImageTk,Image
import urllib.request
import time
import threading
import re

YT = YouTube
root= Tk()
RES = StringVar(value='720p')
FORMAT = StringVar(value='mp4')
THREADS = []
PIC = None
frame = LabelFrame(root, padx=20,pady=50)
FIRST_TIME = True


def main():
    frame.pack(padx=0, pady=0)
    box = Entry(frame, width=100 )
    box.insert(0,'enter url:    ')
    box.grid(row=7, column=0, columnspan=4, padx=5, pady=20 )
    submit = Button(frame, text='check url',command=lambda:thread_manager(handshake_link,[box]))
    submit.grid(row=7,column=4)
    photo_display('placeholder.png')
    #thread_manager(thumbnail_changer,[])
     
def handshake_link(input_box):
    global YT
    haystack = input_box.get()
    search = "https://www.youtube.com/.*"
    try:
        link = re.search(search, haystack).group()
        print(link)
        YT = YouTube(link) 
        thumbnail_changer() 
        
    except:
        print('failed to conect to url')
    clearDisplay(input_box)
    
    display_options()
    input_box.insert(0,'linking sucsesfull pick your res and click on image to download')

def display_options():
    
    rez = Label(frame,text='Resoulution:')
    rez.grid(row=0,column=3)
    pattern = '\"(\d+)p\"'
    results = re.findall(pattern,str(YT.streams.filter(progressive=True)))
    
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
        'audio','mp4'
    ]
    dl = Label(frame, text='download:')
    dl.grid(row=0,column=0)
    num = 1
    for option in download_options:
        x = Radiobutton(frame ,text=option,variable=FORMAT, value=option)
        x.grid(row=num, column= 0)
        num += 1
    print(str(FORMAT))

def download_time():
    print('im here')
    if FORMAT.get() == 'mp4':
        print('mp4')
        vid = YT.streams.filter(res = RES.get(),  progressive = True ).first()
        print('download started')
        vid.download('./videos/')
        print('download complete')
    elif FORMAT.get() == 'audio':
        audio = YT.streams.filter(only_audio=True).first()
        print('download started')
        audio.download('./videos/')
        print('download complete')

def thread_manager(target,args ,self_destruct=True ):
    botbot = len(THREADS)
    print('botbot' + str(botbot) + ' has joined the chat')

    THREADS.append(threading.Thread(target=target, args=args , daemon=self_destruct)) 
    THREADS[botbot].start()

def thumbnail_changer():
        urllib.request.urlretrieve(YT.thumbnail_url, 'gui/beep.jpg' )
        photo_display('beep.jpg')

def photo_display(fileName):
    global FIRST_TIME
    if not FIRST_TIME:
        PIC.delete(0,END)
    img = Image.open('gui/' + fileName).resize((300,200))
    test_img = ImageTk.PhotoImage(img)
    pic = Button(frame, image=test_img, command=lambda:thread_manager(download_time,[],False))
    pic.image = test_img
    pic.grid(row=0,column=2, columnspan =1, rowspan=6)
    PIC = pic

def clearDisplay(display):
    display.delete(0, END)



main()
root.mainloop()
threading._shutdown()