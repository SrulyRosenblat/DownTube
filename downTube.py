import sys
from PyQt5.QtWidgets import QApplication
from vdgui import videoDownloaderGui
def main():
    app = QApplication(sys.argv)
    window = videoDownloaderGui()
    window.show()
    sys.exit(app.exec())
    return

if __name__ == "__main__":              
    main()