from googleapiclient.discovery import build
import key


def main():
    YT = youtubeConnect(key.key)
    playlists = YT.playlist_search('never ending story') 
    for playlist in playlists:
        print(playlist.title)
        for vid in playlist.videos:
            print(vid.title)
        
class videoobject():
    '''
    takes a youtube api video object as a input and outputs cleaned up data
    '''
    def __init__(self,video, thumbnailQuality='medium'):
        videoInfo = video['snippet']
        thumbnail = videoInfo['thumbnails']
        self.url = 'https://www.youtube.com/watch?v=' + video['id']
        self.title = videoInfo['title']
        self.description = videoInfo['description']
        self.date = videoInfo['publishedAt']
        self.channel = videoInfo['channelTitle']
        try :
            self.playlistid = video['playlistId']
        except:
            self.playlistId = None
    
        try:
            self.thumbnailLink = thumbnail[thumbnailQuality]['url']
            self.thumbnailWidth = thumbnail[thumbnailQuality]['width']
            self.thumbnailHeight = thumbnail[thumbnailQuality]['height']
        except:
            print(f"Thumbnail quality {thumbnailQuality} is unavailible defaulted to 'default' availible options are: 'default', 'medium', 'high', 'maxres' ")
            self.thumbnailLink = thumbnail['default']['url']
            self.thumbnailWidth = thumbnail['default']['width']
            self.thumbnailHeight = thumbnail['default']['height']

    def __str__(self):
        return f'title: {self.title},\nurl: {self.url},\ndescription: {self.description},\ndate: {self.date},\nchannel: {self.channel},\nthumbnailLink: {self.thumbnailLink},\nthumbnailWidth: {self.thumbnailWidth},\nthumbnailHeight: {self.thumbnailHeight}'


class playlistobject():
    '''
    takes a youtube api playlist id object as a input and outputs cleaned up data
    '''
    def __init__(self,playlist,thumbnailQuality = 'medium'):
        yt = youtubeConnect(key.key)
        self.id = playlist['id']['playlistId']
        playlistInfo = playlist['snippet']
        self.title = playlistInfo['title']
        self.description = playlistInfo['description']
        self.channel = playlistInfo['channelTitle']
        self.date = playlistInfo['publishedAt']
        thumbnail = playlistInfo['thumbnails']
        try:
            self.thumbnailLink = thumbnail[thumbnailQuality]['url']
            self.thumbnailWidth = thumbnail[thumbnailQuality]['width']
            self.thumbnailHeight = thumbnail[thumbnailQuality]['height']
        except:
            print(f"Thumbnail quality {thumbnailQuality} is unavailible defaulted to 'default' availible options are: 'default', 'medium', 'high'")
            self.thumbnailLink = thumbnail['default']['url']
            self.thumbnailWidth = thumbnail['default']['width']
            self.thumbnailHeight = thumbnail['default']['height']
        self.videos = []
        request = yt.api.playlistItems().list(part="snippet",maxResults=30,playlistId=self.id)
        self.videoCount = 0
        for vidInfo in request.execute()['items']:
            video = yt.video_by_url(vidInfo['snippet']['resourceId']['videoId'])
            self.videos.append(video) 
            self.videoCount += 1

        
    def __str__(self):
        return f'title: {self.title},\nid: {self.id}\ndescription: {self.description},\ndate: {self.date},\nchannel: {self.channel},\nthumbnailLink: {self.thumbnailLink},\nthumbnailWidth: {self.thumbnailWidth},\nthumbnailHeight: {self.thumbnailHeight},\nvideoCount: {self.videoCount}'
class youtubeConnect():

    def __init__(self,key):
        '''
        add a youtube api key and connect to the api
        '''
        self.api = build('youtube','v3', developerKey=key)
        
    def channel_info(self, username, info = 'statistics' ):
        '''
        get channel info in the form of dictionery
        '''
        data = self.api.channels().list(
            part = info,
            forUsername = username
        )
        pass


    def video_by_url(self, url):
        video = self.api.videos().list(part="snippet",id=url).execute()['items'][0]
        return videoobject(video)


    def video_search(self,querry):
        data = self.api.search().list(
            part = "snippet",
            order = "relevance",
            q = querry,
            type = "video"
         )
        li = []
        for videoData in data.execute()['items']:
            videoUrl = videoData['id']['videoId']
            video = self.video_by_url(videoUrl)
            li.append(video)
        return li


    def playlist_search(self,querry):
        '''
        returns a list of playlists based off the querry
        '''
        request = self.api.search().list(part="snippet",q="never ending story",type="playlist")
        response = request.execute()
        playists = []
        for playlist in response['items']:
            playists.append(playlistobject(playlist))
        return playists


if __name__ == "__main__":
    main()