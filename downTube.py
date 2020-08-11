from pytube import YouTube
import tubered as tr
# from PIL import ImageTk,Image
# import urllib.request
# import time
# import threading
# import re
# from moviepy.editor import *
def main():
    vids = tr.handshake_link('what does the fox say')
    if type(vids) == list:
        num = 0
        for vid in vids:
            print(vid.title)
            vid.title = f'bob{num}'
            print(vid.title)
            num += 1
    else:
        print(vids.title)
        
    return

if __name__ == "__main__":              
    main()