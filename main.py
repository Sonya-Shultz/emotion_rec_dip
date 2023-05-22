import PyQt5
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import *
import sys
import tempfile
import os
import warnings

from CNNsClass.CNN import CNN
from GUI.EnterDataDialog import EnterDataDialog
from GUI.GuiWindow import GuiWindow
from GUI.Language import LENG
if not sys.warnoptions:
    warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)


if __name__ == '__main__':
    sys.stdout = tempfile.TemporaryFile()
    sys.stderr = tempfile.TemporaryFile()
    try:
        os.mkdir("./text_res")
    except OSError as error:
        pass
    CNN()
    LENG()
    app = QApplication(sys.argv)
    _id = QFontDatabase.addApplicationFont("./Styles/AdventPro-VariableFont_wdth,wght.ttf")
    win = GuiWindow()
    custom_font = QFont('Advent Pro', int(win.height_p*0.02))
    app.setFont(custom_font)
    with open("./Styles/style.css", 'r') as file:
        sheet = file.read()
    app.setStyleSheet(sheet)
    choose = EnterDataDialog(win)
    if not choose.exec_():
        sys.exit(0)
    win.set_data(choose)
    win.show()
    sys.exit(app.exec_())

