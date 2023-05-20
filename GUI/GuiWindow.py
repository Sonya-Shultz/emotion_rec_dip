import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt

from GUI.DataController import DataController
from GUI.EnterDataDialog import EnterDataDialog
from GUI.Language import LENG


class GuiWindow(QMainWindow):

    def __init__(self, parent=None):
        super(GuiWindow, self).__init__(parent)
        self.move(50, 50)
        self.resize(1280, 720)
        self.data_type = 0  # 0-video+audio, 1-video without audio, 2-audio from video, 3-audio, 4-photo
        self.is_from_file = True
        self.save_to_file = False
        self.show_all_data = False
        self.file_name = ""

        self.lb = QLabel(LENG.elem.SYSTEM_MESS_TMP[1], self)
        self.lb.show()

        self.btn = QPushButton(LENG.elem.BTNS_TEXTs[3], self)
        self.btn.move(750, 60)
        self.btn.clicked.connect(self.on_click_back)
        self.btn.adjustSize()

        self.button_exit = QPushButton(LENG.elem.BTNS_TEXTs[2], self)
        self.button_exit.move(750, 120)
        self.button_exit.clicked.connect(self.on_click_close)
        self.button_exit.adjustSize()

        self.lbl = QLabel("", self)
        self.lbl.move(0, 0)
        self.lbl.resize(20, 700)

    def on_click_close(self):
        self.close()

    def on_click_back(self):
        self.hide()
        choose = EnterDataDialog()
        if not choose.exec_():  # 'reject': user pressed 'Cancel', so quit
            sys.exit(0)
        self.set_data(choose)
        self.show()

    def show(self) -> None:
        super().show()
        DataController.comp_data_controller(self)

    def set_data(self, data):
        self.data_type = data.data_type
        self.is_from_file = data.is_from_file
        self.save_to_file = data.save_to_file
        self.show_all_data = data.show_all_data
        self.file_name = data.file_name


