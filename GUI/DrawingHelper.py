import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPen, QFont, QColor

from DataProcessing.ResultData import ResultData


class DrawingHelper:
    @staticmethod
    def __init__():
        pass

    @staticmethod
    def from_arr_to_pixelmap(data, height):
        h, w, comp = data.shape
        bytesPerLine = 3 * w
        QImg = QImage(
            data,
            w,
            h,
            bytesPerLine,
            QImage.Format_RGB888
        )
        pixmap = QPixmap.fromImage(QImg)
        pixmap = pixmap.scaledToHeight(height)
        scale = 700.0 / h
        return pixmap, scale

    @staticmethod
    def create_pen_n_font(pi, color=(13, 13, 255), pen_w=3, f_size=14, f_family='Times'):
        pen = QPen(QColor(color[0], color[1], color[2]))
        pen.setWidth(pen_w)
        pi.setPen(pen)
        font = QFont()
        font.setFamily(f_family)
        font.setPointSize(f_size)
        pi.setFont(font)

    @staticmethod
    def audio_to_pixelmap(data):
        data = np.array(((data + 80)/80.0 * 255).astype(np.int8))
        data = np.stack((data,) * 3, axis=-1)
        pixmap, scale = DrawingHelper.from_arr_to_pixelmap(data, 700)
        return pixmap, scale



