import sys
import threading
import ctypes

from PyQt5.QtWidgets import *

from GUI.DataController import DataController
from GUI.EnterDataDialog import EnterDataDialog
from GUI.Language import LENG


class GuiWindow(QMainWindow):

    def __init__(self, parent=None):
        super(GuiWindow, self).__init__(parent)
        self.height_p = ctypes.windll.user32.GetSystemMetrics(1)*0.8
        self.width_p = ctypes.windll.user32.GetSystemMetrics(0)*0.8
        self.pos_start = [self.width_p*.01, 0.0, 0.0]
        self.sound_lvl = 0.3
        self.res_show_thread = None
        self.move(self.width_p*.1, self.height_p*.1)
        self.setFixedSize(self.width_p, self.height_p)
        self.data_type = 0  # 0-video+audio, 1-video without audio, 2-audio from video, 3-audio, 4-photo
        self.is_from_file = True
        self.save_to_file = False
        self.show_all_data = False
        self.file_name = ""

        self.lb = QLabel(LENG.elem.SYSTEM_MESS_TMP[1], self)

        self.btn = QPushButton(LENG.elem.BTNS_TEXTs[3], self)
        self.btn.clicked.connect(self.on_click_back)

        self.button_exit = QPushButton(LENG.elem.BTNS_TEXTs[2], self)
        self.button_exit.clicked.connect(self.on_click_close)

        self.button_again = QPushButton(LENG.elem.BTNS_TEXTs[4], self)
        self.button_again.clicked.connect(self.on_click_repeat)

        self.lbl_img = QLabel("", self)

        self.lbl_au = QLabel("", self)
        self.set_text(LENG.elem.NAME[0])

    def set_text(self, language):
        LENG.change_language(language)
        pos = self.width_p * .01
        self.lb.setText(LENG.elem.SYSTEM_MESS_TMP[1])
        self.lb.adjustSize()
        self.lb.move(self.width_p*.01, self.height_p*.01)
        self.lb.show()
        pos += self.lb.width() + self.width_p*0.02

        self.btn.setText(LENG.elem.BTNS_TEXTs[3])
        self.btn.adjustSize()
        pos = int(self.width_p * 0.99) - self.btn.width()
        self.btn.move(pos, self.height_p * .01)

        self.button_exit.setText(LENG.elem.BTNS_TEXTs[2])
        self.button_exit.adjustSize()
        pos -= (self.button_exit.width() + self.width_p * 0.02)
        self.button_exit.move(pos, self.height_p * .01)

        self.button_again.setText(LENG.elem.BTNS_TEXTs[4])
        self.button_again.adjustSize()
        pos -= (self.button_again.width() + self.width_p * 0.02)
        self.button_again.move(pos, self.height_p*.01)

        pos = self.height_p*.02 + self.btn.height()

        self.pos_start = [self.pos_start[0], pos, 0.0]

        self.lbl_img.move(self.pos_start[0], self.pos_start[1])
        self.lbl_img.resize(0, 0)
        self.lbl_au.move(self.pos_start[0], self.pos_start[1])
        self.lbl_au.resize(0, 0)

    def closeEvent(self, event):
        DataController.stop()
        event.accept()

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
        choose = EnterDataDialog(self)
        if not choose.exec_():  # 'reject': user pressed 'Cancel', so quit
            sys.exit(0)
        self.set_data(choose)
        self.show()

    def show(self) -> None:
        super().show()
        DataController.interrupt = False
        self.lb.setText(LENG.elem.SYSTEM_MESS_TMP[1])
        self.lb.adjustSize()
        self.lb.show()
        rs = threading.Thread(target=lambda w=self: DataController.comp_data_controller(w))
        rs.start()
        self.set_text(LENG.elem.NAME[0])

    def set_data(self, data):
        self.data_type = data.data_type
        self.is_from_file = data.is_from_file
        self.save_to_file = data.save_to_file
        self.show_all_data = data.show_all_data
        self.file_name = data.file_name


