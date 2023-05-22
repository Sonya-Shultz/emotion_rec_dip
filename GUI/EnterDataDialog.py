import ctypes

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from GUI.Language import LENG


class EnterDataDialog(QDialog):

    def __init__(self, parent=None):
        super(EnterDataDialog, self).__init__(parent)
        self.height_p = ctypes.windll.user32.GetSystemMetrics(1)*0.8
        self.width_p = ctypes.windll.user32.GetSystemMetrics(0)*0.8
        self.data_type = 0  # 0-video+audio, 1-video without audio, 2-audio from video, 3-audio, 4-photo
        self.is_from_file = True
        self.save_to_file = False
        self.show_all_data = False
        self.all_ed_comp = []
        self.file_name = ""

        self.button = None
        self.button_file = None
        self.button_exit = None
        self.type_list = None
        self.lang_list = None
        self.checkbox_rt = None
        self.checkbox_sf = None
        self.checkbox_shd = None
        self.filename_lbl = None
        self.error_lbl = None

        self.setup_main_gui()

    def setup_main_gui(self):
        self.setWindowTitle(LENG.elem.WINDOW_NAMES[0])
        self.move(self.width_p * .1, self.height_p * .1)
        self.setFixedSize(self.width_p, self.height_p)

        self.button = QPushButton(LENG.elem.BTNS_TEXTs[0], self)
        self.button.clicked.connect(self.on_click_process)
        self.all_ed_comp.append(self.button)

        self.button_file = QPushButton(LENG.elem.BTNS_TEXTs[1], self)
        self.button_file.clicked.connect(self.on_click_file_choose)
        self.all_ed_comp.append(self.button_file)

        self.button_exit = QPushButton(LENG.elem.BTNS_TEXTs[2], self)
        self.button_exit.clicked.connect(self.on_click_close)

        self.filename_lbl = QLabel(LENG.elem.LBL_TEXTs[0], self)
        self.filename_lbl.show()

        self.type_list = QComboBox(self)
        self.type_list.addItems(LENG.elem.DATA_TYPES)
        self.type_list.currentTextChanged.connect(self.select_from_drop)
        self.all_ed_comp.append(self.type_list)
        self.type_list.show()

        self.checkbox_rt = QCheckBox(LENG.elem.CHECKBOX_TEXTs[0], self)
        self.checkbox_rt.stateChanged.connect(lambda state, d=self.type_list, f=self.button_file: self.rt_check(state, d, f))
        self.all_ed_comp.append(self.checkbox_rt)

        self.checkbox_sf = QCheckBox(LENG.elem.CHECKBOX_TEXTs[1], self)
        self.checkbox_sf.stateChanged.connect(self.sf_check)
        self.all_ed_comp.append(self.checkbox_sf)

        self.checkbox_shd = QCheckBox(LENG.elem.CHECKBOX_TEXTs[2], self)
        self.checkbox_shd.stateChanged.connect(self.shd_check)
        self.all_ed_comp.append(self.checkbox_shd)

        self.lang_list = QComboBox(self)
        self.lang_list.addItems(LENG.elem.NAME)

        self.lang_list.currentTextChanged.connect(self.select_lang_from_drop)
        self.all_ed_comp.append(self.lang_list)
        self.lang_list.show()

        self.error_lbl = QLabel("", self)
        self.error_lbl.setFont(QFont('Advent Pro', int(self.height_p*0.025)))
        self.error_lbl.setStyleSheet("color: red")

        self.set_texts(LENG.elem.NAME[0])

    def set_texts(self, language):
        LENG.change_language(language)
        posy = self.height_p*.05

        self.button_file.setText(LENG.elem.BTNS_TEXTs[1])
        self.button_file.adjustSize()
        self.button_file.move(self.width_p/2 - self.button_file.width()/2, posy)
        posy += self.height_p*.01 + self.button_file.height()

        self.filename_lbl.setText(LENG.elem.LBL_TEXTs[0]+self.file_name)
        self.filename_lbl.setFont(QFont('Advent Pro', int(self.height_p * 0.015)))
        self.filename_lbl.adjustSize()
        self.filename_lbl.move(self.width_p/2 - self.filename_lbl.width()/2, posy)
        posy += self.height_p*.03 + self.filename_lbl.height()

        self.checkbox_rt.setText(LENG.elem.CHECKBOX_TEXTs[0])
        self.checkbox_rt.adjustSize()
        self.checkbox_rt.move(self.width_p/2 - self.checkbox_rt.width()/2, posy)
        posy += self.height_p * .01 + self.checkbox_rt.height()

        self.checkbox_sf.setText(LENG.elem.CHECKBOX_TEXTs[1])
        self.checkbox_sf.adjustSize()
        self.checkbox_sf.move(self.width_p/2 - self.checkbox_sf.width()/2, posy)
        posy += self.height_p * .01 + self.checkbox_sf.height()

        self.checkbox_shd.setText(LENG.elem.CHECKBOX_TEXTs[2])
        self.checkbox_shd.adjustSize()
        self.checkbox_shd.move(self.width_p/2 - self.checkbox_shd.width()/2, posy)
        posy += self.height_p * .03 + self.checkbox_shd.height()

        self.type_list.blockSignals(True)
        self.type_list.clear()
        if self.is_from_file:
            self.type_list.addItems(LENG.elem.DATA_TYPES)
        else:
            self.type_list.addItems(LENG.elem.RT_DATA_TYPES)
        self.type_list.adjustSize()
        self.type_list.move(self.width_p/2 - self.type_list.width()/2, posy)
        self.type_list.blockSignals(False)

        self.button.setText(LENG.elem.BTNS_TEXTs[0])
        self.button.adjustSize()
        self.button.move(self.width_p/2 - self.button.width()/2, self.height_p*0.7 - self.button.height())

        self.button_exit.setText(LENG.elem.BTNS_TEXTs[2])
        self.button_exit.adjustSize()
        self.button_exit.move(self.width_p/2 - self.button_exit.width()/2, self.height_p * .95
                              - self.button_exit.height())

        self.lang_list.adjustSize()
        self.lang_list.move(self.width_p * .98 - self.lang_list.width(), self.height_p * .02)
        self.error_lbl.setText("")

        self.parent().set_text(language)

    def set_all_enabled_sate(self, d):
        for el in self.all_ed_comp:
            el.setEnabled(d)

    def on_click_file_choose(self):
        self.open_files()
        self.filename_lbl.setText(LENG.elem.LBL_TEXTs[0] + self.file_name)
        self.filename_lbl.adjustSize()
        self.filename_lbl.move(self.width_p / 2 - self.filename_lbl.width() / 2,
                               self.height_p * .06 + self.button_file.height())

    def on_click_close(self):
        self.reject()

    def on_click_process(self):

        if self.is_from_file:
            self.set_all_enabled_sate(False)
            self.error_lbl.setText(LENG.elem.SYSTEM_MESS_TMP[0])
            self.error_lbl.adjustSize()
            self.error_lbl.move(self.width_p/2 - self.error_lbl.width()/2, self.height_p*0.55 - self.error_lbl.height())
            self.error_lbl.show()
            if self.check_params():
                self.error_lbl.setText(LENG.elem.SYSTEM_MESS_TMP[1])
                self.error_lbl.adjustSize()
                self.error_lbl.move(self.width_p / 2 - self.error_lbl.width() / 2,
                                    self.height_p * 0.55 - self.error_lbl.height())
                self.set_all_enabled_sate(True)
                self.accept()
            else:
                self.error_lbl.setText(LENG.elem.SYSTEM_MESS_ERR[1])
                self.error_lbl.adjustSize()
                self.error_lbl.move(self.width_p / 2 - self.error_lbl.width() / 2,
                                    self.height_p * 0.55 - self.error_lbl.height())
            self.set_all_enabled_sate(True)
        else:
            self.set_all_enabled_sate(False)
            self.error_lbl.setText(LENG.elem.SYSTEM_MESS_TMP[2])
            self.error_lbl.adjustSize()
            self.error_lbl.move(self.width_p / 2 - self.error_lbl.width() / 2,
                                self.height_p * 0.55 - self.error_lbl.height())
            self.set_all_enabled_sate(True)
            self.accept()

    def rt_check(self, st, tp_list, btn_file):
        self.is_from_file = not (st == Qt.Checked)
        tp_list.blockSignals(True)
        tp_list.clear()
        if self.is_from_file:
            tp_list.addItems(LENG.elem.DATA_TYPES)
            btn_file.setEnabled(True)
            self.filename_lbl.setText(LENG.elem.LBL_TEXTs[0] + self.file_name)
        else:
            tp_list.addItems(LENG.elem.RT_DATA_TYPES)
            btn_file.setEnabled(False)
            self.filename_lbl.setText("")
        tp_list.blockSignals(False)

    def sf_check(self, st):
        self.save_to_file = st == Qt.Checked

    def shd_check(self, st):
        self.show_all_data = st == Qt.Checked

    def select_from_drop(self, s):  # s is a str
        self.data_type = LENG.elem.DATA_TYPES.index(s)

    def select_lang_from_drop(self, s):
        self.set_texts(s)

    def open_files(self):
        d = QFileDialog()
        self.setStyleSheet("QTreeView {font: "+str(int(self.height_p*0.012))+"pt \"Arial\";}")
        options = d.Options()
        options |= d.DontUseNativeDialog
        file, _ = d.getOpenFileName(self, LENG.elem.WINDOW_NAMES[2], "",
                                                "All Files (*);;", options=options)
        if file:
            self.file_name = file

    def check_params(self):
        resol = {0: [".mp4"], 1: [".mp4"], 2: [".mp4"], 3: [".mp3", ".wav"], 4: [".jpg", ".png"]}
        if self.data_type in resol and self.file_name != "":
            r = resol[self.data_type]
            for el in r:
                st = self.file_name.lower()
                if st.endswith(el):
                    return True
            return False
        else:
            return False

