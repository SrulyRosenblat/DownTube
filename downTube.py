from pytube import YouTube

print('pytube loaded')
link = input('enter a url to download:  ')

yt = YouTube(link)
vid = yt.streams.filter(res ='360p',  progressive = True ).first()

print('downloading..')

# the title of the video is 'youtube'
vid.download(r'C:\Users\sruls\OneDrive\Desktop\yt-dl', yt.title)

print('download complete of "' + yt.title + '"')


# yt = YouTube('https://www.youtube.com/watch?v=trKjYdBASyQ')
# al = yt.streams.all()
# rez = yt.streams.filter(res ='720p',  progressive = True)
# #res = yt.streams.filter()
# for stream in rez:
#     print(stream)
