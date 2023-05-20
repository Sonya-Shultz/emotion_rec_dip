from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QRect

from DataProcessing.PrepareData import PrepareData
from DataProcessing.ResultData import ResultData
from GUI.Language import LENG


class DataController:
    @staticmethod
    def comp_data_controller(wind):
        res = None
        res2 = None
        data = None
        print(wind.is_from_file, wind.data_type)
        if wind.is_from_file:
            if wind.data_type == 0:
                data, res, res2 = PrepareData.for_video(wind.file_name)
            elif wind.data_type == 1:
                data, _, res2 = PrepareData.for_video(wind.file_name, with_sound=False)
            elif wind.data_type == 2:
                data, res, _ = PrepareData.for_video(wind.file_name, with_video=False)
            elif wind.data_type == 3:
                data, res = PrepareData.for_audio(wind.file_name)
            else:
                data, res = PrepareData.for_photo(wind.file_name)
                DataController.__show_img(wind.lbl, data.raw_data, res)
            wind.lb.setText(LENG.elem.SYSTEM_MESS_GOOD[0])
            if wind.save_to_file:
                if res:
                    res.write_to_file()
                if res2:
                    res2.write_to_file()
        else:
            PrepareData.for_video_real_time()

    @staticmethod
    def __show_img(wind, data, res):
        h, w, comp = data.shape
        bytesPerLine = comp * w
        QImg = QImage(
            data,
            w,
            h,
            bytesPerLine,
            QImage.Format_RGB888
        )
        pixmap = QPixmap.fromImage(QImg)
        pixmap = pixmap.scaledToHeight(700)
        scale = 700.0/h

        painterInstance = QPainter(pixmap)
        penRectangle = QPen(Qt.red)
        penRectangle.setWidth(3)
        painterInstance.setPen(penRectangle)
        font = QFont()
        font.setFamily('Times')
        font.setBold(False)
        font.setPointSize(14)
        painterInstance.setFont(font)

        for i in range(len(res.position)):
            painterInstance.drawRect(int(res.position[i][0] * scale), int(res.position[i][1] * scale),
                                     int(res.position[i][2] * scale), int(res.position[i][3] * scale))
            text = ResultData.find_max_em(res.res_arr[i])[0]
            text = text[0] + " " + str(text[1]) + "%"
            painterInstance.drawText(int(res.position[i][0] * scale)-10, int(res.position[i][1] * scale)-10,
                                     text)
        painterInstance.end()
        del painterInstance

        wind.setPixmap(pixmap)
        wind.adjustSize()
        del pixmap
