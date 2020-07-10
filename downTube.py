from pytube import YouTube
from tkinter import *
from PIL import ImageTk,Image
import urllib.request
import time
import threading
import re

YT = YouTube
root= Tk()
root.iconbitmap('gui/logo.ico')
root.title(' DownTube')
root.resizable(0,0)
RES = StringVar(value='720p')
FORMAT = StringVar(value='mp4')
TEXT = StringVar(value='enter url:    ')
THREADS = []
PIC = None
frame = LabelFrame(root, padx=20,pady=50)
res_frame = LabelFrame(frame)
FIRST_TIME = True
ENTRY_BOX = Entry(frame, width=100, text=TEXT )
submit = Button(frame, text='check url',command=lambda:thread_manager(handshake_link,[]))

def main():
    global FIRST_TIME
    frame.pack(padx=0, pady=0)
    ENTRY_BOX.grid(row=7, column=0, columnspan=4, padx=5, pady=20 )
    submit.grid(row=7,column=4)
    photo_display('youtube-logo.jpg')
    FIRST_TIME = False
    #thread_manager(thumbnail_changer,[])
     
def handshake_link():
    global YT
    submit.config(state=DISABLED)
    haystack = ENTRY_BOX.get()
    search = "https://www.youtube.com/.*"
    try:
        link = re.search(search, haystack).group()
        print(link)
        YT = YouTube(link) 
        thumbnail_changer() 
        TEXT.set('connected to url pick your format / resoulution click thumbnail to download')
    except:
        TEXT.set('failed to conect to url')
    submit.config(state=NORMAL)
    display_options()
    
def display_options():
    
    pattern = '\"(\d+)p\"'
    streams = YT.streams.filter(progressive=True)
    results = re.findall(pattern,str(streams))
    
    results = list(map(int, results))
    results.sort(reverse=True)
    results = [str(result) + 'p' for result in results]

    rez = Label(frame,text='Resoulution:')
    rez.grid(row=0,column=3)
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
    res_frame.grid(column=0,row=0)
    dl = Label(frame, text='download:')
    dl.grid(row=0,column=0)
    num = 1
    for option in download_options:
        x = Radiobutton(frame ,text=option,variable=FORMAT, value=option)
        x.grid(row=num, column= 0)
        num += 1
    print(str(FORMAT))
    
def download_time():
    if FORMAT.get() == 'mp4':
        vid = YT.streams.filter(res = RES.get(),  progressive = True ).first()
        TEXT.set('downloading..')
        PIC.config(state=DISABLED)
        vid.download('./videos/')
        PIC.config(state=NORMAL)
        TEXT.set('download complete')

    elif FORMAT.get() == 'audio':
        audio = YT.streams.filter(only_audio=True).first()
        TEXT.set('downloading..')
        PIC.config(state=DISABLED)
        audio.download('./videos/')
        PIC.config(state=NORMAL)
        TEXT.set('download complete')

def thread_manager(target,args ,self_destruct=True ):
    botbot = len(THREADS)
    print('botbot' + str(botbot) + ' has joined the chat')

    THREADS.append(threading.Thread(target=target, args=args , daemon=self_destruct)) 
    THREADS[botbot].start()

def thumbnail_changer():
    print(urllib.request.urlretrieve(YT.thumbnail_url, 'gui/beep.jpg' ))
    photo_display('beep.jpg')
   

def photo_display(fileName):
    global FIRST_TIME
    global PIC
    if not FIRST_TIME:
        PIC.destroy()
        instruction = Label(frame, text='click on thumbnail to download:')
        instruction.grid(row=0, column=2)
    img = Image.open('gui/' + fileName).resize((300,200))
    test_img = ImageTk.PhotoImage(img)
    pic = Button(frame, image=test_img, command=lambda:thread_manager(download_time,[],False))
    pic.image = test_img
    pic.grid(row=1,column=2, columnspan =1, rowspan=6)
    PIC = pic

def clearDisplay(display):
    display.delete(0, END)



main()
root.mainloop()
threading._shutdown()