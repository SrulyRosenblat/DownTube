from pytube import YouTube
link = input('enter a url to download:  ')
yt = YouTube(link)
choice = input('enter the resoulution:  ')
vid = None
while vid is None:
    choice = input('resoulution invalid enter again:  ')
    vid = yt.streams.filter(res = choice,  progressive = True ).first()

print('downloading..')

vid.download(r'C:\Users\sruls\OneDrive\Desktop\yt-dl', yt.title)

print('download complete of "' + yt.title + '"')