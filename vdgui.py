from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys
import functools

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
        self.grid = QGridLayout()
        self.grid.setAlignment(Qt.AlignCenter)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
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

        description = QTextBrowser()
        description.setText('rtgkeirjguermjmetuijmgiu\njguiwrhnuignwuhnuhn\nuj4wtjiu4hju8qh8h')
        description.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        description.setStatusTip('the description of the current video')

        searchbar = QLineEdit()
        searchbar.setPlaceholderText('search for video or enter url')
        searchbar.setStyleSheet("border: 2px solid black;border-radius: 10px;font-size: 36px;")
        searchbar.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        searchbar.setStatusTip('search for a video')
    

        downloadbtn = QPushButton()
        downloadbtn.setText('Download')
        downloadbtn.setStyleSheet('background-color: rgb(0, 85, 255); border: 1px solid black;border-radius: 10px;font-size: 30px;color: white;padding: 5px 15px;')
        downloadbtn.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        downloadbtn.setCursor(QCursor(Qt.PointingHandCursor))
        downloadbtn.setStatusTip('download the current video')

        backbtn = QPushButton()
        backbtn.setText('<<<')
        backbtn.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        backbtn.setCursor(QCursor(Qt.PointingHandCursor))
        backbtn.setStatusTip('go to last video')
        
        nextbtn = QPushButton()
        nextbtn.setText('>>>')
        nextbtn.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        nextbtn.setCursor(QCursor(Qt.PointingHandCursor))
        nextbtn.setStatusTip('go to next video')

        picture = QLabel()
        img = QPixmap('./gui/thumbnail.jpg')
        img = img.scaled(1280,720, Qt.KeepAspectRatio)
        picture.setPixmap(img)
        picture.setStatusTip('the thumbnail of the video selected')

        title = QLabel()
        title.setText('oppo finally did it')
        title.setStatusTip('the title of the selected video')

        videoType = QComboBox()
        videoType.addItems(['video and audio', 'audio only'])
        videoType.setCursor(QCursor(Qt.PointingHandCursor))
        videoType.setStatusTip('pick your download format')

        searchbarSpacer = QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Maximum)
        descriptionSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        downloadSpacer = QSpacerItem(20, 30, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.grid.addWidget(videoType,3,9,1,2)
        self.grid.addWidget(title,3,5,1,3)
        self.grid.addWidget(picture,4,5,3,6)
        self.grid.addWidget(backbtn,7,5,1,3)
        self.grid.addWidget(nextbtn,7,8,1,3)
        self.grid.addItem(downloadSpacer,8,6,1,0)
        self.grid.addWidget(downloadbtn,9,5,1,6)
        self.grid.addItem(searchbarSpacer,10,4,1,0)
        self.grid.addWidget(searchbar,11,3,1,11)
        self.grid.addItem(descriptionSpacer,3,11,0,3)
        self.grid.addWidget(description,3,14,4,3)
        self.grid.addWidget(slider,4,0,3,4)

app = QApplication(sys.argv)
window = videoDownloaderGui()
window.show()
sys.exit(app.exec())