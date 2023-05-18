from PyQt5.QtWidgets import *
import sys
import warnings

from CNNsClass.CNN import CNN
from GUI.EnterDataDialog import EnterDataDialog
from GUI.GuiWindow import GuiWindow
from GUI.Language import LENG
if not sys.warnoptions:
    warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)


if __name__ == '__main__':
    CNN()
    LENG()
    #PrepareData.for_photo("test.jpg")
    #PrepareData.for_video_real_time()
    #PrepareData.for_audio("test.mp3")
    #PrepareData.for_video("test.MP4")
    app = QApplication(sys.argv)
    choose = EnterDataDialog()
    if not choose.exec_():  # 'reject': user pressed 'Cancel', so quit
        sys.exit(-1)
    win = GuiWindow()
    win.set_data(choose)
    win.show()
    sys.exit(app.exec_())

