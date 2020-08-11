from googleapiclient.discovery import build


def main():
    yt = youtubeConnect(key.key)
    vids = yt.video_search(input('enter video: '))
    for vid in vids:
        print(vid.title + ' ' + vid.url)
        
class videoobject():
    '''
    takes a youtube api video object as a input and outputs cleaned up data
    '''
    def __init__(self,video, thumbnailQuality='medium', playlistid=None):
        videoInfo = video['snippet']
        thumbnail = videoInfo['thumbnails']
        self.url = 'https://www.youtube.com/watch?v=' + video['id']
        self.title = videoInfo['title']
        self.description = videoInfo['description']
        self.date = videoInfo['publishedAt']
        self.channel = videoInfo['channelTitle']
        self.playlistid = playlistid
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
class youtubeConnect():

    def __init__(self,key):
        '''
        add a youtube api key and connect to the api
        '''
        self.key = key
        self.api = build('youtube','v3', developerKey=self.key)
        
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
        # playlistList = self.api.search().list(part="snippet",q="pizza",type="playlist").execute()['items']
        # playlistIds = [x['id']['playlistId'] for x in playlistList]
        # playlistsVidIds = []
        # count = 0
        # for playId in playlistIds:
        #     vidIds = []
        #     vidIds.append(playlistList[count])
        #     for vid in self.api.playlistItems().list(part="contentDetails", playlistId = playId ).execute()['items']:
        #         vidIds.append(vid['contentDetails']['videoId']) 
        #     playlistsVidIds.append(vidIds)
        #     count += 1

        # for playlist in playlistsVidIds:
        #     videos = []
        #     for video in self.api.videos().list(part="snippet",id=playlist[1:]).execute()['items']:
        #        videos.append(videoobject(video)) 
        #     yield playlist[0] , videos
        pass


if __name__ == "__main__":
    main()