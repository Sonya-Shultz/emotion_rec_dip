import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
from GUI.Language import LENG
from DataProcessing.PrepareData import PrepareData


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

    def show(self) -> None:
        super().show()
        self.comp_data_controller()

    def set_data(self, data):
        self.data_type = data.data_type
        self.is_from_file = data.is_from_file
        self.save_to_file = data.save_to_file
        self.show_all_data = data.show_all_data
        self.file_name = data.file_name

    def comp_data_controller(self):
        res = None
        res2 = None
        print(self.is_from_file, self.data_type)
        if self.is_from_file:
            if self.data_type == 0:
                res, res2 = PrepareData.for_video(self.file_name)
            elif self.data_type == 1:
                _, res2 = PrepareData.for_video(self.file_name, with_sound=False)
            elif self.data_type == 2:
                res, _ = PrepareData.for_video(self.file_name, with_video=False)
            elif self.data_type == 3:
                res = PrepareData.for_audio(self.file_name)
            else:
                res = PrepareData.for_photo(self.file_name)
            self.lb.setText(LENG.elem.SYSTEM_MESS_GOOD[0])
            if res:
                res.write_to_file()
            if res2:
                res2.write_to_file()
        else:
            PrepareData.for_video_real_time()

