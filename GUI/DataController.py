import threading
import time

import librosa
import numpy as np
import simpleaudio as sa
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QRect

from DataProcessing.PrepareData import PrepareData
from DataProcessing.ResultData import ResultData
from GUI.DrawingHelper import DrawingHelper
from GUI.Language import LENG


class DataController:
    res = None
    res2 = None
    data = None
    interrupt = False
    play_obj = None

    @staticmethod
    def __init__():
        pass

    @staticmethod
    def stop():
        DataController.interrupt = True
        if DataController.play_obj:
            DataController.play_obj.stop()
            DataController.play_obj = None
        DataController.res = None
        DataController.res2 = None
        DataController.data = None

    @staticmethod
    def show_res(wind):
        if wind.is_from_file:
            if wind.data_type == 0:
                DataController.__show_video(wind, DataController.data, DataController.res2, DataController.res, lvl=wind.sound_lvl)
            elif wind.data_type == 1:
                DataController.__show_video(wind, DataController.data, DataController.res2, DataController.res, with_audio=False)
            elif wind.data_type == 2:
                DataController.__show_audio(wind.lbl_au, DataController.data.audioPart.raw_data,
                                            DataController.data.audioPart.sr, DataController.res, wind.sound_lvl)
            elif wind.data_type == 3:
                DataController.__show_audio(wind.lbl_au, DataController.data.raw_data,
                                            DataController.data.sr, DataController.res, wind.sound_lvl)
            else:
                DataController.__show_img(wind.lbl_img, DataController.data.raw_data, DataController.res)
            wind.lb.setText(LENG.elem.SYSTEM_MESS_GOOD[0])
            if wind.save_to_file:
                if DataController.res:
                    DataController.res.write_to_file()
                if DataController.res2:
                    DataController.res2.write_to_file()

            wind.button_again.setEnabled(True)
        else:
            PrepareData.for_video_real_time()

    @staticmethod
    def comp_data_controller(wind):
        wind.button_again.setEnabled(False)
        if wind.is_from_file:
            try:
                if wind.data_type == 0:
                    DataController.data, DataController.res, DataController.res2 \
                        = PrepareData.for_video(wind.file_name)
                elif wind.data_type == 1:
                    DataController.data, _, DataController.res2 \
                        = PrepareData.for_video(wind.file_name, with_sound=False)
                elif wind.data_type == 2:
                    DataController.data, DataController.res, _ \
                        = PrepareData.for_video(wind.file_name, with_video=False)
                elif wind.data_type == 3:
                    DataController.data, DataController.res \
                        = PrepareData.for_audio(wind.file_name)
                else:
                    DataController.data, DataController.res = PrepareData.for_photo(wind.file_name)
                wind.lb.setText(LENG.elem.SYSTEM_MESS_GOOD[0])
                wind.res_show_thread = threading.Thread(target=lambda w=wind: DataController.show_res(w))
                wind.res_show_thread.start()
            except Exception as e:
                wind.lb.setText(LENG.elem.SYSTEM_MESS_ERR[0]+"\n"+str(e))
        else:
            PrepareData.for_video_real_time()

    @staticmethod
    def __play_audio(data, sr, lvl=1.0):
        d = data * 32767 * lvl / np.max(np.abs(data))
        d = d.astype(np.int16)
        DataController.play_obj = sa.play_buffer(d, 1, 2, sr)

    @staticmethod
    def __show_audio(lb, data, sr, res, lvl, poss=(0, 0)):
        ind = 0
        ind_c = 0
        time_cur = time.time_ns()
        while ind < len(data) and not DataController.interrupt:
            ind_t = ind
            ind = min(ind + int(sr * ResultData.part_len), len(data))
            d = data[ind_t:ind]
            DataController.__play_audio(d, sr, lvl=lvl)
            spectrogram = librosa.feature.melspectrogram(y=d, sr=sr)
            spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
            spectrogram = spectrogram.astype(np.float32)

            pixmap, scale = DrawingHelper.audio_to_pixelmap(spectrogram)

            painter = QPainter(pixmap)
            DrawingHelper.create_pen_n_font(painter, color=(255, 13, 13))

            text = ResultData.find_max_em(res.res_arr[ind_c])[0]
            text = text[0] + " " + str(text[1]) + "%"
            painter.drawText(50, 50, text)

            painter.end()
            del painter

            lb.setPixmap(pixmap)
            lb.adjustSize()
            lb.move(poss[0], poss[1])
            del pixmap
            ind_c += 1
            timer_sleep = max(0.005, ResultData.part_len - max((time.time_ns() - time_cur) / 1e9, 0.0))
            time.sleep(timer_sleep-0.005)
            time_cur = time.time_ns()

    @staticmethod
    def __show_img(lb, data, res, poss=(0, 0)):
        pixmap, scale = DrawingHelper.from_arr_to_pixelmap(data, 700)

        painter = QPainter(pixmap)
        DrawingHelper.create_pen_n_font(painter)

        for i in range(len(res.position)):
            painter.drawRect(int(res.position[i][0] * scale), int(res.position[i][1] * scale),
                                        int(res.position[i][2] * scale), int(res.position[i][3] * scale))
            text = ResultData.find_max_em(res.res_arr[i])[0]
            text = text[0] + " " + str(text[1]) + "%"
            painter.drawText(int(res.position[i][0] * scale)-10, int(res.position[i][1] * scale)-10, text)
        painter.end()
        del painter

        lb.setPixmap(pixmap)
        lb.adjustSize()
        lb.move(poss[0], poss[1])
        del pixmap

    @staticmethod
    def __show_video(wind, data, res_v, res_a, with_audio=True, lvl=1.0):
        ad = data.audioPart
        vd = data.photoPart
        th2 = threading.Thread(target=lambda w=wind, v=vd, r=res_v: DataController.__func_t(w, v, r))
        th2.start()
        pos2 = int(700/len(vd[0].raw_data)*len(vd[0].raw_data[0]))
        th = threading.Thread(target=lambda l=wind.lbl_au, d=ad.raw_data, sr=ad.sr, r=res_a, p=pos2, lv=lvl:
                            DataController.__show_audio(l, d, sr, r, lv, (p, 0)))
        if with_audio:
            th.start()
            th.join()
        th2.join()

    @staticmethod
    def __func_t(wind, vd, res_v):
        i = 0
        c_time = time.time_ns()
        while i < len(vd) and not DataController.interrupt:
            DataController.__show_img(wind.lbl_img, vd[i].raw_data, res_v[i])
            i += 1
            t = max(0.005, ResultData.spf - max((time.time_ns() - c_time) / 1e9, 0.0))
            time.sleep(t-0.005)
            c_time = time.time_ns()

