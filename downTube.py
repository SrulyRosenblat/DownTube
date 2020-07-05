from pytube import YouTube
link = input('enter a url to download:  ')
yt = YouTube(link)
choice = input('enter the resoulution:  ')
while True:
    vid = yt.streams.filter(res = choice,  progressive = True ).first()
    if vid:
        break
    choice = input('resoulution unavailable enter again:  ')
print('downloading..')

vid.download(r'C:\Users\sruls\OneDrive\Desktop\yt-dl', yt.title)

print('download complete of "' + yt.title + '"')