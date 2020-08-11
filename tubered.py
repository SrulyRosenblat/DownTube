import ytsearch
import key
import re
YT = ytsearch.youtubeConnect(key.key)
def handshake_link(text):
    '''
    get video from input
    '''
    if (link := find_link(text)):
       return YT.video_by_url(link)
    else:
        return YT.video_search(text)
    
def find_link(text):
    """
    looks through the text for a youtube link
    """
    link = re.match("https://www\.youtube\.com/watch\?v=(.*)",text)
    if link:
        return link.group(1)
    else:
        return False

def download_time(video_url):
    '''
    download video or mp3
    '''
    # global DOWNLOADING
    # if FORMAT.get() == 'mp4':
    #     vid = YT.streams.filter(res = RES.get(),  progressive = True ).first()
    #     # to start download animation
    #     DOWNLOADING = TRUE
    #     vid.download('./videos/')
        
    # elif FORMAT.get() == 'audio':
    #     audio = YT.streams.filter(only_audio=True).first()
    #     # to start download animation
    #     DOWNLOADING = TRUE
    #     audio.download('./videos/')

    # PIC.config(state=NORMAL)

    # DOWNLOADING = False
    # TEXT.set('download complete')

def thread_manager(target,args=[] ,self_destruct=True ):
    '''
    send out threads
    '''

    # botbot = len(THREADS)
    # print('botbot' + str(botbot) + ' has joined the chat')
    # THREADS.append(threading.Thread(target=target, args=args , daemon=self_destruct)) 
    # THREADS[botbot].start()
    pass

def thumbnail_changer():
    '''
    change thumnail display 
    '''
    pass
def photo_display(fileName):
    '''
    display central photo
    '''
    pass

def download_ing():
    '''
    the logic behind the progress bars
    '''
    pass           