
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor , QPixmap
from PyQt5.QtCore import Qt, QThreadPool
import sys
import functools
import ytsearch
import key
from urllib.request import urlretrieve
from pytube import YouTube
from worker import Worker, makebot
import time
from functools import partial
class videoDownloaderGui(QMainWindow):
    def __init__(self, parent=None):
        '''
        sets up videoDownloader gui
        '''
        super().__init__(parent)
        self.setGeometry(100, 100, 2000, 1250)
        self.setWindowTitle('youtube downloader')
        central = QWidget()
        self.setCentralWidget(central)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)      
        self.index = 0
        self.videos = []

        self.progressbars = []
        self.downloading  = []
        self.downloadTitles = []

        self.status = []
        self.botbots = []
        self.threadpool = QThreadPool()
        self.startbot = self.threadpool.start
        self.grid = QGridLayout()
        self.grid.setAlignment(Qt.AlignCenter)
        self.api = None
        self.resolution = '720p'
        self.setupGui()
        central.setLayout(self.grid)
        
        # connectBot = Worker(self.connectToApi) 
        # self.startbot(connectBot)
        self.makeAndSendBot(self.connectToApi)
        

    def connectToApi(self):
        self.api = ytsearch.youtubeConnect(key.key)

    def setupGui(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileLocation = QAction("&file locaition", self)
        fileLocation.setShortcut("Ctrl+F")
        fileLocation.setStatusTip('set the file location for videos')
        resoulutionMenu = mainMenu.addMenu('&resoulution')
        for res in ['360p','720p']:
            resoulution = QAction(f"&{res}", self)
            resoulution.setStatusTip(f'set the download size to {res}')
            resoulution.triggered.connect(partial(self.setRes,res))
            resoulutionMenu.addAction(resoulution)
        fileMenu.addAction(fileLocation)
      
        self.description = QTextBrowser()
        self.description.setText('description:\ntype somthing in to look for videos\nenjoy 🤞')
        self.description.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.description.setStatusTip('the description of the current video')

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText('search for video or enter url')
        self.searchbar.setStyleSheet("border: 2px solid black;border-radius: 10px;font-size: 36px;")
        self.searchbar.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        self.searchbar.setStatusTip('search for a video')
        self.searchbar.returnPressed.connect(self.searchVids)
    

        self.downloadbtn = QPushButton()
        self.downloadbtn.setText('Download')
        self.downloadbtn.setStyleSheet('QPushButton {background-color: darkgray; border: 1px solid black;border-radius: 10px;font-size: 30px;color: white;padding: 5px 15px;}')
        self.downloadbtn.setEnabled(False)
        self.downloadbtn.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        self.downloadbtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.downloadbtn.setStatusTip('download the current video')
        self.downloadbtn.clicked.connect(lambda:self.makeAndSendBot(self.downloadVideo,startedFunc=self.downloadBtnSetup,progressFunc=self.showBars,finishedFunc=self.downloadBtnSetup,errorFunc = self.downloadFailed))

        self.backbtn = QPushButton()
        self.backbtn.setText('<<<')
        self.backbtn.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred))
        self.backbtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.backbtn.clicked.connect(lambda:self.changeIndex(-1))
        self.backbtn.setStatusTip('go to last video')
        self.backbtn.setEnabled(False)
        
        self.nextbtn = QPushButton()
        self.nextbtn.setText('>>>')
        self.nextbtn.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred))
        self.nextbtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.nextbtn.clicked.connect(lambda:self.changeIndex(1))
        self.nextbtn.setStatusTip('go to next video')
        self.nextbtn.setEnabled(False)
        

        self.picture = QLabel()
        img = QPixmap('./gui/youtube-logo.jpg')
        img = img.scaled(1280,720)
        self.picture.setPixmap(img)
        self.picture.setStatusTip('the thumbnail of the video selected')

        self.titleDisplay = QLabel()
        self.titleDisplay.setText('search for a video')
        self.titleDisplay.setStatusTip('the title of the selected video')

        self.videoType = QComboBox()
        self.videoType.addItems(['video and audio', 'audio only'])
        self.videoType.setCursor(QCursor(Qt.PointingHandCursor))
        self.videoType.setStatusTip('pick your download format') 
        

        
        self.progressGrid = QGridLayout()
        progressSpacer = QSpacerItem(20,200,QSizePolicy.Minimum,QSizePolicy.MinimumExpanding)

        for i in range(10):
            if i  % 2 == 0:
                title = QLabel()
                title.setWordWrap(True)
                self.progressGrid.addWidget(title,i,0,1,2)
                self.downloadTitles.append(title)
                title.setHidden(True)
            else:
                prog = QProgressBar()
                prog.setValue(100)
                self.progressGrid.addWidget(prog,i,0,1,2)     
                self.progressbars.append(prog)
                prog.setHidden(True)
        
        self.progressGrid.addItem(progressSpacer,20,0)

        searchbarSpacer = QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Preferred)
        descriptionSpacer = QSpacerItem(325,20, QSizePolicy.Preferred, QSizePolicy.Minimum)
        downloadSpacer = QSpacerItem(20, 25, QSizePolicy.Maximum, QSizePolicy.Preferred)
        progressGridSpacer = QSpacerItem(200,20, QSizePolicy.Preferred, QSizePolicy.Minimum)
        

        self.grid.addWidget(self.videoType,3,9,1,2)
        self.grid.addItem(progressGridSpacer,1,0,rowSpan=1,columnSpan=2 )
        #self.grid.addWidget(self.resPicker,3,1,2,2)
        self.grid.addWidget(self.titleDisplay,3,5,1,3)
        self.grid.addWidget(self.picture,4,5,3,6)
        self.grid.addWidget(self.backbtn,7,5,1,3)
        self.grid.addWidget(self.nextbtn,7,8,1,3)
        self.grid.addItem(downloadSpacer,8,6,rowSpan=1,columnSpan=1 )
        self.grid.addWidget(self.downloadbtn,9,5,1,6)
        self.grid.addItem(searchbarSpacer,10,4,rowSpan=1,columnSpan=1)
        self.grid.addWidget(self.searchbar,11,3,1,11)
        self.grid.addItem(descriptionSpacer,8,14,rowSpan=1,columnSpan=4)
        self.grid.addWidget(self.description,3,14,4,3)
        
        self.grid.addLayout(self.progressGrid,4,0,3,4)
    
    def setRes(self,resoulution):
        self.resolution = resoulution

    def searchVids(self):
        while not self.api:
            time.sleep(.05)
        self.videos = self.api.video_search(self.searchbar.text(),limit=10,thumbnailQuality='maxres',defultQuality='high')
            
        if len(self.videos) >= 1:
            self.status = ['download' for x in self.videos]
            self.downloadThumbnails()
            self.setVideo()
            if not self.index + 1 >= len(self.videos):
                self.nextbtn.setEnabled(True)
        else:
            self.searchbar.setText('')
            self.searchbar.setPlaceholderText('no videos availaible that match the search')
            # todo make it not crash here

    def downloadThumbnails(self):        
        count = 0
        for vid in self.videos:
            urlretrieve(vid.thumbnailLink, f'gui/thumbnails/thumbnail{count}.jpg' )
            count += 1
       
    def setVideo(self):
        img = QPixmap(f'gui/thumbnails/thumbnail{self.index}.jpg')
        img = img.scaled(1280,720,transformMode=Qt.FastTransformation)
        self.picture.setPixmap(img)
        self.description.setText(self.videos[self.index].description)
        self.setTitleText(self.videos[self.index].title)
        self.downloadBtnSetup()
        
    def setTitleText(self,text):
        if len(text) >= 40:
            self.titleDisplay.setText(text[:40] + '...')
        else:
            self.titleDisplay.setText(text)

    def changeIndex(self,num):
        self.index += num
        if self.index + 1 == len(self.videos):
            self.nextbtn.setEnabled(False)
            self.backbtn.setEnabled(True)
        elif self.index == 0:
            self.backbtn.setEnabled(False)
            self.nextbtn.setEnabled(True)
        else:
            self.backbtn.setEnabled(True)
            self.nextbtn.setEnabled(True)

        self.setVideo()
    
    def downloadBtnSetup(self):
        state = self.status[self.index]

        if state == 'downloading':
            self.downloadbtn.setText('Downloading..')
            bgColor = 'darkgray'
            bgColorHover = 'gray'
            bgColorPressed = 'light gray'
            self.downloadbtn.setEnabled(False)
        elif  state == 'downloaded':
            self.downloadbtn.setText('Download again')
            bgColor = 'gray'
            bgColorHover = 'lightgray'
            bgColorPressed = 'lightgray'
            self.downloadbtn.setEnabled(True)
 
        elif state == 'download':
            self.downloadbtn.setText('Download')
            bgColor = 'rgb(0, 85, 255)'
            bgColorHover = 'rgb(89, 111, 255)'
            bgColorPressed = 'lightblue'
            self.downloadbtn.setEnabled(True)
        elif state == 'error':
            self.downloadbtn.setText('Download Failed')
            bgColor = 'red'
            bgColorHover = 'orange'
            bgColorPressed = 'darkred'
            self.downloadbtn.setEnabled(True)
 

        self.downloadbtn.setStyleSheet('QPushButton {background-color: %s; border: 1px solid black;border-radius: 10px;font-size: 30px;color: white;padding: 5px 15px;}''QPushButton:pressed { background-color: %s }''QPushButton:hover { background-color: %s }'%(bgColor,bgColorPressed,bgColorHover) )
        
        #self.downloadbtn.setEnabled(False)
        
    def downloadVideo(self):
        index = self.index
        video = self.videos[index]
        self.status[index] = 'downloading'
        print('downloading ' + video.url)
        yt = YouTube(video.url,on_progress_callback=self.progress_func)
        vid = yt.streams.filter(res=self.resolution,progressive=True).first()
        vid.download('./videos')
        self.status[index] = 'downloaded'
        print('download complete')
    
    def downloadFailed(self, error):
        print(error)
        self.status[self.index] = 'error'
        self.downloadBtnSetup()


    def progress_func(self, stream, chunk, bytes_remaining):
        size = stream.filesize
        progress = (float(abs(bytes_remaining-size)/size))*float(100)
        self.bot.signals.progress.emit((stream , int(progress)))  


    def showBars(self, info):
        '''
        display all progressBars in list
        '''
        
        stream,progress = info
        if stream not in self.downloading:
            print(stream)
            self.downloading.append(stream)
            index = self.downloading.index(stream)
            self.downloadTitles[index].setText(stream.title)
            self.downloadTitles[index].setHidden(False)
        else:
            index = self.downloading.index(stream)
        self.progressbars[index].setValue(progress)
        self.progressbars[index].setHidden(False)
        if progress == 100:
            self.downloadTitles[index].setHidden(True)
            self.progressbars[index].setHidden(True)


    def makeAndSendBot(self,func,*args,**kwargs):
        self.bot = makebot(func,*args,**kwargs) 
        self.startbot(self.bot)

app = QApplication(sys.argv)
window = videoDownloaderGui()
window.show()
sys.exit(app.exec())