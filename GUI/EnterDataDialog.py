from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from GUI.Language import LENG


class EnterDataDialog(QDialog):

    def __init__(self, parent=None):
        super(EnterDataDialog, self).__init__(parent)
        self.data_type = 0  # 0-video+audio, 1-video without audio, 2-audio from video, 3-audio, 4-photo
        self.is_from_file = True
        self.save_to_file = False
        self.show_all_data = False
        self.all_ed_comp = []
        self.__btn_arr = []
        self.__combo_box = None
        self.__filename_lbl = None
        self.__checkbox_arr = []
        self.file_name = ""
        self.setup_main_gui()

    def setup_main_gui(self):
        self.setWindowTitle(LENG.elem.WINDOW_NAMES[0])
        self.move(50, 50)
        self.resize(1280, 720)

        button = QPushButton(LENG.elem.BTNS_TEXTs[0], self)
        button.move(550, 230)
        button.clicked.connect(self.on_click_process)
        self.all_ed_comp.append(button)
        button.adjustSize()

        button_file = QPushButton(LENG.elem.BTNS_TEXTs[1], self)
        button_file.move(550, 60)
        button_file.clicked.connect(self.on_click_file_choose)
        self.all_ed_comp.append(button_file)
        button_file.adjustSize()

        button_exit = QPushButton(LENG.elem.BTNS_TEXTs[2], self)
        button_exit.move(550, 290)
        button_exit.clicked.connect(self.on_click_close)
        button_exit.adjustSize()

        lbl = QLabel(LENG.elem.LBL_TEXTs[0], self)
        lbl.move(750, 60)
        lbl.show()
        self.__filename_lbl = lbl

        type_list = QComboBox(self)
        type_list.move(550, 200)
        type_list.addItems(LENG.elem.DATA_TYPES)
        type_list.currentTextChanged.connect(self.select_from_drop)
        type_list.adjustSize()
        self.all_ed_comp.append(type_list)
        type_list.show()

        checkbox_rt = QCheckBox(LENG.elem.CHECKBOX_TEXTs[0], self)
        checkbox_rt.move(550, 90)
        checkbox_rt.stateChanged.connect(lambda state, d=type_list, f=button_file: self.rt_check(state, d, f))
        checkbox_rt.adjustSize()
        self.all_ed_comp.append(checkbox_rt)
        checkbox_sf = QCheckBox(LENG.elem.CHECKBOX_TEXTs[1], self)
        checkbox_sf.move(550, 120)
        checkbox_sf.stateChanged.connect(self.sf_check)
        checkbox_sf.adjustSize()
        self.all_ed_comp.append(checkbox_sf)
        checkbox_shd = QCheckBox(LENG.elem.CHECKBOX_TEXTs[2], self)
        checkbox_shd.move(550, 150)
        checkbox_shd.stateChanged.connect(self.shd_check)
        checkbox_shd.adjustSize()
        self.all_ed_comp.append(checkbox_shd)

        lang_list = QComboBox(self)
        lang_list.move(1000, 600)
        lang_list.addItems(LENG.LANG_LIST)
        self.__btn_arr = [button, button_file, button_exit]
        self.__combo_box = type_list
        self.__checkbox_arr = [checkbox_rt, checkbox_sf, checkbox_shd]

        lang_list.currentTextChanged.connect(self.select_lang_from_drop)
        lang_list.adjustSize()
        self.all_ed_comp.append(lang_list)
        lang_list.show()

    def set_texts(self, language):
        LENG.change_language(language)
        for i in range(len(self.__btn_arr)):
            self.__btn_arr[i].setText(LENG.elem.BTNS_TEXTs[i])
        self.__combo_box.blockSignals(True)
        self.__combo_box.clear()
        if self.is_from_file:
            self.__combo_box.addItems(LENG.elem.DATA_TYPES)
        else:
            self.__combo_box.addItems(LENG.elem.RT_DATA_TYPES)
        self.__combo_box.blockSignals(False)
        for i in range(len(self.__checkbox_arr)):
            self.__checkbox_arr[i].setText(LENG.elem.CHECKBOX_TEXTs[i])
        self.__filename_lbl.setText(LENG.elem.LBL_TEXTs[0]+self.file_name)

    def set_all_enabled_sate(self, d):
        for el in self.all_ed_comp:
            el.setEnabled(d)

    def on_click_file_choose(self):
        self.open_files()
        self.__filename_lbl.setText(LENG.elem.LBL_TEXTs[0] + self.file_name)
        self.__filename_lbl.adjustSize()

    def on_click_close(self):
        self.reject()

    def on_click_process(self):
        lb = QLabel("", self)
        lb.move(550, 330)
        if self.is_from_file:
            self.set_all_enabled_sate(False)
            lb.setText(LENG.elem.SYSTEM_MESS_TMP[0])
            lb.adjustSize()
            lb.show()
            if self.check_params():
                lb.setText(LENG.elem.SYSTEM_MESS_TMP[1])
                lb.adjustSize()
                self.set_all_enabled_sate(True)
                self.accept()
            else:
                lb.setText(LENG.elem.SYSTEM_MESS_ERR[1])
                lb.adjustSize()
            self.set_all_enabled_sate(True)
        else:
            self.set_all_enabled_sate(False)
            lbl = QLabel(LENG.elem.SYSTEM_MESS_TMP[2], self)
            lbl.move(550, 30)
            lbl.show()
            self.set_all_enabled_sate(True)
            self.accept()

    def rt_check(self, st, tp_list, btn_file):
        self.is_from_file = not (st == Qt.Checked)
        tp_list.blockSignals(True)
        tp_list.clear()
        if self.is_from_file:
            tp_list.addItems(LENG.elem.DATA_TYPES)
            btn_file.setEnabled(True)
            self.__filename_lbl.setText(LENG.elem.LBL_TEXTs[0] + self.file_name)
        else:
            tp_list.addItems(LENG.elem.RT_DATA_TYPES)
            btn_file.setEnabled(False)
            self.__filename_lbl.setText("")
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
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
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

