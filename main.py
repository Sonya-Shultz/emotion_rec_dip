from PyQt5.QtWidgets import *
import sys
import warnings

from CNNsClass.CNN import CNN
from GUI.GuiWindow import GuiWindow

if not sys.warnoptions:
    warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)


if __name__ == '__main__':
    CNN()
    #PrepareData.for_photo("test.jpg")
    #PrepareData.for_video_real_time()
    #PrepareData.for_audio("test.mp3")
    #PrepareData.for_video("test.MP4")
    app = QApplication(sys.argv)
    win = GuiWindow()
    win.show()
    sys.exit(app.exec_())

