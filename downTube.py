from pytube import YouTube
from tkinter import *
from PIL import ImageTk,Image
import urllib.request
import time
import threading
import re
from youtubesearchpython import SearchVideos



YT = YouTube
root= Tk()
root.iconbitmap('gui/logo.ico')
root.title(' DownTube')
root.resizable(0,0)
RES = StringVar(value='720p')
FORMAT = StringVar(value='mp4')
TEXT = StringVar(value='enter url or title:    ')
THREADS = []
PIC = None
frame = LabelFrame(root, padx=20,pady=50)
res_frame = LabelFrame(frame)
FIRST_TIME = True
DOWNLOADING = False
ENTRY_BOX = Entry(frame, width=100, text=TEXT )
submit = Button(frame, text='Enter',command=lambda:thread_manager(handshake_link))


def main():
    global FIRST_TIME
    set_up_tkinter()
    FIRST_TIME = False

def set_up_tkinter():
    frame.pack(padx=0, pady=0)
    ENTRY_BOX.grid(row=7, column=0, columnspan=4, padx=5, pady=20 )
    submit.grid(row=7,column=4)
    photo_display('youtube-logo.jpg')
    thread_manager(target=download_ing)
    
def handshake_link():
    global YT
    # makes it so user cant click button
    submit.config(state=DISABLED)
    link = text_box_search("https://www.youtube.com/.*")
    try:
        if link:
            YT = YouTube(link)
           
        else:
            text = text_box_search(':(.*)')
            if text:
                text2 = text_box_search(':(.*\S)')
                if text2:
                    search = SearchVideos(text, offset = 1, mode = "list", max_results = 2)
                else:
                    submit.config(state=NORMAL)
                    print('search empty')
                    return
            else:
                search = SearchVideos(ENTRY_BOX.get(), offset = 1, mode = "list", max_results = 2)
            results = search.result()
            YT = YouTube(results[0][2])
        thumbnail_changer() 
        TEXT.set('connected to video, pick your format / resoulution and then click thumbnail to download:')
    except:
        TEXT.set('failed to conect to video enter again:')
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
    
def download_time():
    global DOWNLOADING
    if FORMAT.get() == 'mp4':
        vid = YT.streams.filter(res = RES.get(),  progressive = True ).first()
        DOWNLOADING = TRUE
        PIC.config(state=DISABLED)
        vid.download('./videos/')
        
    elif FORMAT.get() == 'audio':
        audio = YT.streams.filter(only_audio=True).first()
        DOWNLOADING = TRUE
        PIC.config(state=DISABLED)
        audio.download('./videos/')
    PIC.config(state=NORMAL)
    DOWNLOADING = False
    TEXT.set('download complete')

def thread_manager(target,args=[] ,self_destruct=True ):
    botbot = len(THREADS)
    print('botbot' + str(botbot) + ' has joined the chat')
    THREADS.append(threading.Thread(target=target, args=args , daemon=self_destruct)) 
    THREADS[botbot].start()

def thumbnail_changer():
    urllib.request.urlretrieve(YT.thumbnail_url, 'gui/thumbnail.jpg' )
    photo_display('thumbnail.jpg')
   
def photo_display(fileName):
    global FIRST_TIME
    global PIC
    if not FIRST_TIME:
        PIC.destroy()
        instruction = Label(frame, text='click on thumbnail to download:')
        instruction.grid(row=0, column=2)
    img = Image.open('gui/' + fileName).resize((300,200))
    if DOWNLOADING:
        pass
    else:
        thumbnail = ImageTk.PhotoImage(img)
    pic = Button(frame, image=thumbnail, command=lambda:thread_manager(download_time,[],False))
    pic.image = thumbnail
    pic.grid(row=1,column=2, columnspan =1, rowspan=6)
    PIC = pic

def clearDisplay(display):
    display.delete(0, END)

def text_box_search(needle):
    result = re.search(needle, ENTRY_BOX.get())
    if result == None:
        return False
    else:
        return result.group()

def download_ing():
    while True:
        time.sleep(1)
        while DOWNLOADING:
            TEXT.set('Downloading.')
            time.sleep(.5) 
            if DOWNLOADING:
                TEXT.set('Downloading...')
                time.sleep(.5)
                
main()
root.mainloop()
threading._shutdown()