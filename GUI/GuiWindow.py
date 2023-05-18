import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt

from DataProcessing.PrepareData import PrepareData


class GuiWindow(QMainWindow):
    all_ed_comp = []
    file_name = ""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_type = 0  # 0-video+audio, 1-video-audio, 2-audio, 3-photo
        self.is_from_file = True
        self.save_to_file = False
        self.show_all_data = False
        self.setup_main_gui()

    def setup_main_gui(self):
        self.setWindowTitle("Main Menu")
        self.move(50, 50)
        self.resize(1280, 720)

        lbl = QLabel('Оберіть вхідні дані:', self)
        lbl.move(550, 30)
        lbl.adjustSize()

        button = QPushButton('ОБРОБИТИ', self)
        button.setToolTip('Натисніть сюди після вибору файлів')
        button.move(550, 60)
        button.clicked.connect(self.on_click_process)
        self.all_ed_comp.append(button)
        button.adjustSize()

        button_file = QPushButton('ОБРАТИ ФАЙЛ', self)
        button_file.setToolTip('Натисніть сюди для вибору файлу')
        button_file.move(550, 60)
        button_file.clicked.connect(self.on_click_file_choose)
        self.all_ed_comp.append(button_file)
        button_file.adjustSize()

        type_list = QComboBox(self)
        type_list.move(550, 200)
        type_list.addItems(["Відео зі звуком", "Лише відео", "Лише звук", "Фото"])
        type_list.currentTextChanged.connect(self.select_from_drop)
        type_list.adjustSize()
        self.all_ed_comp.append(type_list)
        type_list.show()

        checkbox_rt = QCheckBox("В режимі реального часу", self)
        checkbox_rt.move(550, 90)
        checkbox_rt.stateChanged.connect(lambda state, d=type_list, f=button_file: self.rt_check(state, d, f))
        checkbox_rt.adjustSize()
        self.all_ed_comp.append(checkbox_rt)
        checkbox_sf = QCheckBox("Зберегти до файлу", self)
        checkbox_sf.move(550, 120)
        checkbox_sf.stateChanged.connect(self.sf_check)
        checkbox_sf.adjustSize()
        self.all_ed_comp.append(checkbox_sf)
        checkbox_shd = QCheckBox("Показати повний результат", self)
        checkbox_shd.move(550, 150)
        checkbox_shd.stateChanged.connect(self.shd_check)
        checkbox_shd.adjustSize()
        self.all_ed_comp.append(checkbox_shd)

    def set_all_edit_sate(self, d):
        for el in self.all_ed_comp:
            el.setEnabled(d)

    def on_click_file_choose(self):
        self.open_files()

    @pyqtSlot()
    def on_click_process(self):
        if self.is_from_file:
            self.set_all_edit_sate(False)
            lbl = QLabel('Перевірка файлів', self)
            lbl.move(550, 200)
            lbl.adjustSize()
            lbl.show()
            if True:
                lbl.setText("Йде обробка...")
                lbl.adjustSize()
                try:
                    PrepareData.for_photo("test.jpg")
                    lbl.setText("Готово!")
                    self.set_all_edit_sate(True)
                except Exception:
                    lbl.setText("Щось пішло не так при обробці (")
                    lbl.adjustSize()
            else:
                lbl.setText("Обраний файл не підходить до обраного формату")
                lbl.adjustSize()
        else:
            self.set_all_edit_sate(False)
            lbl = QLabel('Запуск пристроїв', self)
            lbl.move(550, 200)
            lbl.show()
            try:
                PrepareData.for_video_real_time()
                lbl.setText("Готово!")
                self.set_all_edit_sate(True)
            except Exception:
                lbl.setText("Щось пішло не так(")

    def rt_check(self, st, tp_list, btn_file):
        self.is_from_file = not (st == Qt.Checked)
        tp_list.clear()
        if self.is_from_file:
            tp_list.addItems(["Відео зі звуком", "Лише відео", "Лише звук", "Фото"])
            btn_file.setEnabled(True)
        else:
            tp_list.addItems(["Відео зі звуком", "Лише відео", "Лише звук"])
            btn_file.setEnabled(False)

    def sf_check(self, st):
        self.save_to_file = st == Qt.Checked

    def shd_check(self, st):
        self.show_all_data = st == Qt.Checked

    def select_from_drop(self, s):  # s is a str
        print(s)

    def open_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if file:
            self.file_name = file
