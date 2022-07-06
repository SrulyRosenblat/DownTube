# DownTube

## a fast and simple way to download youtube videos
a full fledged youtube downloader with support for searching youtube and 
realtime progressbars

*only works on windows* 


## how to download and install
* download the downtube.zip file
* right click on the file you instaled and then click on extract all
* search through the extracted folder and double click on DownTube.exe (the file with the DownTube logo)
* if you want to move the file create a shortcut **do not move the file**

## some of the code behind the project
  ```
      def showBars(self, info):
        '''
        display all progressBars in a list
        '''
        stream,progress = info
        if stream not in self.downloading:
            self.downloadCounter += 1
            self.downloading[stream] = self.downloadCounter % 10
            index = self.downloading[stream]
            self.downloadTitles[index].setText(stream.title)
            self.downloadTitles[index].setHidden(False)
        else:
            index = self.downloading[stream]
        self.progressbars[index].setValue(progress)
        self.progressbars[index].setHidden(False)
        if progress == 100:
            self.downloadTitles[index].setHidden(True)
            self.progressbars[index].setHidden(True)
            self.downloading.pop(stream)
        return
  ```
  600+ lines of code

## pictures
sample 1
![downtube demo picture 1](./demos/bear.jpg?raw=true "Title")

sample 2
![downtube demo picture 2](./demos/phone.jpg?raw=true "Title")


sample 3
![downtube demo picture 3](./demos/tiktok.jpg?raw=true "Title")
