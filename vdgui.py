from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys
import functools
import ytsearch
import key
from urllib.request import urlretrieve
import time
from pytube import YouTube
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
        self.api = ytsearch.youtubeConnect(key.key)
        self.index = 0
        self.videos = []
        self.grid = QGridLayout()
        self.grid.setAlignment(Qt.AlignCenter)
        
        self.setupGui()
        central.setLayout(self.grid)
        
        
    def setupGui(self):
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('&File')
        fileLocation = QAction("&file locaition", self)
        fileLocation.setShortcut("Ctrl+F")
        fileLocation.setStatusTip('set the file location for videos')
        fileMenu.addAction(fileLocation)
        

        slider = QSlider(Qt.Vertical)
        slider.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        slider.setCursor(QCursor(Qt.OpenHandCursor))
        slider.setStatusTip('pick your resoulution')
       # slider.sliderMoved(lambda:slider.setCursor(QCursor(Qt.ClosedHandCursor)))
        #slider.sliderMoved(lambda:slider.setCursor(QCursor(Qt.OpenHandCursor)))

        self.description = QTextBrowser()
        self.description.setText('rtgkeirjguermjmetuijmgiu\njguiwrhnuignwuhnuhn\nuj4wtjiu4hju8qh8h')
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
        self.downloadbtn.setStyleSheet('QPushButton {background-color: rgb(0, 85, 255); border: 1px solid black;border-radius: 10px;font-size: 30px;color: white;padding: 5px 15px;}''QPushButton:pressed { background-color: gray }''QPushButton:hover { background-color: skyblue }')#''QPushButton:pressed { background-color: gray }'
 
        self.downloadbtn.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        self.downloadbtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.downloadbtn.setStatusTip('download the current video')
        self.downloadbtn.clicked.connect(self.downloadVideo)

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
        self.titleDisplay
        self.titleDisplay.setText('oppo finally did it')
        self.titleDisplay.setStatusTip('the title of the selected video')

        self.videoType = QComboBox()
        self.videoType.addItems(['video and audio', 'audio only'])
        self.videoType.setCursor(QCursor(Qt.PointingHandCursor))
        self.videoType.setStatusTip('pick your download format')

        searchbarSpacer = QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Maximum)
        descriptionSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        downloadSpacer = QSpacerItem(20, 30, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.grid.addWidget(self.videoType,3,9,1,2)
        self.grid.addWidget(self.titleDisplay,3,5,1,3)
        self.grid.addWidget(self.picture,4,5,3,6)
        self.grid.addWidget(self.backbtn,7,5,1,3)
        self.grid.addWidget(self.nextbtn,7,8,1,3)
        self.grid.addItem(downloadSpacer,8,6,1,0)
        self.grid.addWidget(self.downloadbtn,9,5,1,6)
        self.grid.addItem(searchbarSpacer,10,4,1,0)
        self.grid.addWidget(self.searchbar,11,3,1,11)
        self.grid.addItem(descriptionSpacer,3,11,0,3)
        self.grid.addWidget(self.description,3,14,4,3)
        self.grid.addWidget(slider,4,0,3,4)


    def searchVids(self):
        self.videos = self.api.video_search(self.searchbar.text(),limit=5,thumbnailQuality='maxres',defultQuality='high')
        self.downloadThumbnails()
        self.setVideo()
        if not self.index + 1 >= len(self.videos):
            self.nextbtn.setEnabled(True)

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
    
    def downloadVideo(self):
        print('downloading' + self.videos[self.index].url)
        yt = YouTube(self.videos[self.index].url)
        vid = yt.streams.filter(progressive=True).first()
        vid.download('./videos')
        
app = QApplication(sys.argv)
window = videoDownloaderGui()
window.show()
sys.exit(app.exec())