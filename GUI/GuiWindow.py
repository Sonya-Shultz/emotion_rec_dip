import sys
import threading

from PyQt5.QtWidgets import *

from GUI.DataController import DataController
from GUI.EnterDataDialog import EnterDataDialog
from GUI.Language import LENG


class GuiWindow(QMainWindow):

    def __init__(self, parent=None):
        super(GuiWindow, self).__init__(parent)
        self.res_show_thread = None
        self.move(50, 50)
        self.resize(1280, 720)
        self.data_type = 0  # 0-video+audio, 1-video without audio, 2-audio from video, 3-audio, 4-photo
        self.is_from_file = True
        self.save_to_file = False
        self.show_all_data = False
        self.file_name = ""
        self.sound_lvl = 0.05

        self.lb = QLabel(LENG.elem.SYSTEM_MESS_TMP[1], self)
        self.lb.show()

        self.btn = QPushButton(LENG.elem.BTNS_TEXTs[3], self)
        self.btn.move(750, 60)
        self.btn.clicked.connect(self.on_click_back)
        self.btn.adjustSize()

        self.button_exit = QPushButton(LENG.elem.BTNS_TEXTs[2], self)
        self.button_exit.move(750, 180)
        self.button_exit.clicked.connect(self.on_click_close)
        self.button_exit.adjustSize()

        self.button_again = QPushButton(LENG.elem.BTNS_TEXTs[4], self)
        self.button_again.move(750, 120)
        self.button_again.clicked.connect(self.on_click_repeat)
        self.button_again.adjustSize()

        self.lbl_img = QLabel("", self)
        self.lbl_img.move(0, 0)
        self.lbl_img.resize(20, 700)

        self.lbl_au = QLabel("", self)
        self.lbl_img.move(0, 0)
        self.lbl_img.resize(20, 700)

    def on_click_repeat(self):
        self.button_again.setEnabled(False)
        self.res_show_thread = threading.Thread(target=lambda d=self: DataController.show_res(d))
        self.res_show_thread.start()

    def on_click_close(self):
        DataController.stop()
        self.close()

    def on_click_back(self):
        self.lbl_img.resize(0, 0)
        self.lbl_au.resize(0, 0)
        DataController.stop()
        self.hide()
        choose = EnterDataDialog()
        if not choose.exec_():  # 'reject': user pressed 'Cancel', so quit
            sys.exit(0)
        self.set_data(choose)
        self.show()

    def show(self) -> None:
        super().show()
        DataController.interrupt = False
        self.lb.setText(LENG.elem.SYSTEM_MESS_TMP[1])
        self.lb.show()
        rs = threading.Thread(target=lambda w=self: DataController.comp_data_controller(w))
        rs.start()

    def set_data(self, data):
        self.data_type = data.data_type
        self.is_from_file = data.is_from_file
        self.save_to_file = data.save_to_file
        self.show_all_data = data.show_all_data
        self.file_name = data.file_name


