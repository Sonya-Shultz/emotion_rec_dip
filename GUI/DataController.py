import threading
import time

import cv2
import librosa
import numpy as np
import pyaudio
import simpleaudio as sa
from PyQt5.QtGui import QPainter

from DataProcessing.PrepareData import PrepareData
from DataProcessing.ResultData import ResultData
from GUI.DrawingHelper import DrawingHelper
from GUI.Language import LENG


class DataController:
    res = None
    res2 = None
    data = None
    data2 = None
    interrupt = False
    play_obj = None
    cap = None

    @staticmethod
    def __init__():
        pass

    @staticmethod
    def stop():
        DataController.interrupt = True
        if DataController.play_obj:
            DataController.play_obj.stop()
            DataController.play_obj = None
        if DataController.cap:
            DataController.cap.release()
            DataController.cap = None
        DataController.res = None
        DataController.res2 = None
        DataController.data = None
        DataController.data2 = None

    @staticmethod
    def show_res(wind):
        if wind.is_from_file:
            if wind.data_type == 0:
                DataController.__show_video(wind, DataController.data2, DataController.res2, DataController.res, lvl=wind.sound_lvl)
            elif wind.data_type == 1:
                DataController.__show_video(wind, DataController.data2, DataController.res2, DataController.res, with_audio=False)
            elif wind.data_type == 2:
                pos = (wind.pos_start[0], wind.pos_start[1])
                DataController.__show_audio(wind, DataController.data.audioPart.raw_data,
                                            DataController.data.audioPart.sr, DataController.res,
                                            wind.sound_lvl, poss=pos)
            elif wind.data_type == 3:
                pos = (wind.pos_start[0], wind.pos_start[1])
                DataController.__show_audio(wind, DataController.data.raw_data,
                                            DataController.data.sr, DataController.res, wind.sound_lvl, poss=pos)
            else:
                DataController.__show_img(wind, DataController.data2.raw_data, DataController.res2)
            wind.lb.setText(LENG.elem.SYSTEM_MESS_GOOD[0])

            wind.button_again.setEnabled(True)

    @staticmethod
    def comp_data_controller(wind):
        wind.button_again.setEnabled(False)
        if wind.is_from_file:
            try:
                if wind.data_type == 0:
                    DataController.data2, DataController.res, DataController.res2 \
                        = PrepareData.for_video(wind.file_name)
                elif wind.data_type == 1:
                    DataController.data2, _, DataController.res2 \
                        = PrepareData.for_video(wind.file_name, with_sound=False)
                elif wind.data_type == 2:
                    DataController.data, DataController.res, _ \
                        = PrepareData.for_video(wind.file_name, with_video=False)
                elif wind.data_type == 3:
                    DataController.data, DataController.res \
                        = PrepareData.for_audio(wind.file_name)
                else:
                    DataController.data2, DataController.res2 = PrepareData.for_photo(wind.file_name)
                wind.lb.setText(LENG.elem.SYSTEM_MESS_GOOD[0])
                wind.res_show_thread = threading.Thread(target=lambda w=wind: DataController.show_res(w))
                wind.res_show_thread.start()
                if wind.save_to_file:
                    if DataController.res:
                        DataController.res.write_to_file()
                    if DataController.res2:
                        DataController.res2.write_to_file()
            except Exception as e:
                wind.lb.setText(LENG.elem.SYSTEM_MESS_ERR[0]+"\n"+str(e))
                wind.lb.adjustSize()
        else:
            try:
                if wind.data_type == 0:
                    th = threading.Thread(target=lambda w=wind: DataController.start_web(w))
                    th.start()
                    pos = (wind.pos_start[0]+wind.lbl_img.width(), wind.pos_start[1])
                    th2 = threading.Thread(target=lambda w=wind, l=wind.lbl_au, lvl=wind.sound_lvl, po=pos:
                                                                        DataController.start_audio(w, l, lvl, pos=po))
                    th2.start()
                elif wind.data_type == 1:
                    th = threading.Thread(target=lambda w=wind: DataController.start_web(w))
                    th.start()
                else:
                    pos = (wind.pos_start[0], wind.pos_start[1])
                    th = threading.Thread(target=lambda w=wind, l=wind.lbl_au, lvl=wind.sound_lvl, po=pos:
                                                                        DataController.start_audio(w, l, lvl, pos=po))
                    th.start()
                    pass
            except Exception as e:
                wind.lb.setText(LENG.elem.SYSTEM_MESS_ERR[0] + "\n" + str(e))
                wind.lb.adjustSize()

    @staticmethod
    def start_web(wind):
        DataController.cap = cv2.VideoCapture(0)
        while not DataController.interrupt:
            ret, img = DataController.cap.read()
            b, g, r = cv2.split(img)
            img = cv2.merge([r, g, b])
            DataController.data2, DataController.res2 = PrepareData.for_photo_data(img)
            th = threading.Thread(target=lambda w=wind, d=DataController.data2.raw_data, r=DataController.res2:
                                                                                    DataController.__show_img(w, d, r))
            th.start()
        wind.lbl_img.resize(0, 0)

    @staticmethod
    def start_audio(wind, lbl, lvl, pos=(0, 0)):
        sr = 22050
        p = pyaudio.PyAudio()
        stream = None
        if DataController.data2:
            pos = (wind.lbl_img.width+wind.pos_start[0], wind.pos_start[1])
        try:
            stream = p.open(format=pyaudio.paFloat32,
                            channels=1,
                            rate=sr,
                            input=True,
                            frames_per_buffer=1024)
            tmp = True
            while not DataController.interrupt:
                frames = []
                for i in range(0, int(sr / 1024 * ResultData.part_len)):
                    if tmp and DataController.data2:
                        pos = (wind.lbl_img.width() + wind.pos_start[0], wind.pos_start[1])
                        tmp = False
                    data = stream.read(1024)
                    tmp_data = np.fromstring(data, dtype=np.float32)
                    frames.append(tmp_data)
                frames = np.hstack(frames)
                if DataController.interrupt:
                    break
                DataController.data, DataController.res = PrepareData.for_audio_data(frames, sr)
                th = threading.Thread(target=lambda w=wind, d=DataController.data.raw_data, s=sr, r=DataController.res,
                                      lv=lvl, p_=pos:
                                      DataController.__show_audio(w, d, s, r, lv, p_))
                th.start()
        except Exception as e:
            wind.lb.setText(LENG.elem.SYSTEM_MESS_ERR[2] + "\n" + str(e))
            wind.lb.adjustSize()
        if stream:
            stream.stop_stream()
            stream.close()
        p.terminate()
        lbl.resize(0, 0)

    @staticmethod
    def __play_audio(data, sr, lvl=1.0):
        d = data * 32767 * lvl / np.max(np.abs(data))
        d = d.astype(np.int16)
        DataController.play_obj = sa.play_buffer(d, 1, 2, sr)

    @staticmethod
    def __show_audio(wind, data, sr, res, lvl, poss=(0, 0)):
        ind = 0
        ind_c = 0
        time_cur = time.time_ns()
        if not res or not data.any():
            return
        if len(res.res_arr) <= 0:
            return
        while ind < len(data) and not DataController.interrupt:
            ind_t = ind
            ind = min(ind + int(sr * ResultData.part_len), len(data))
            d = data[ind_t:ind]
            DataController.__play_audio(d, sr, lvl=lvl)
            spectrogram = librosa.feature.melspectrogram(y=d, sr=sr)
            spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
            spectrogram = spectrogram.astype(np.float32)

            pixmap, scale = DrawingHelper.audio_to_pixelmap(spectrogram, wind.height_p*0.8)

            painter = QPainter(pixmap)
            DrawingHelper.create_pen_n_font(painter, color=(255, 13, 13))
            text = ResultData.find_max_em(res.res_arr[ind_c])[0]
            if wind.show_all_data:
                DataController.show_all_emotion(wind, [res.res_arr[ind_c]], is_audio=True)
            text = text[0] + " " + str(text[1]) + "%"
            painter.drawText(50, 50, text)

            painter.end()
            del painter

            wind.lbl_au.setPixmap(pixmap)
            wind.lbl_au.adjustSize()
            wind.lbl_au.move(poss[0], poss[1])
            del pixmap
            ind_c += 1
            timer_sleep = max(0.005, ResultData.part_len - max((time.time_ns() - time_cur) / 1e9, 0.0))
            time.sleep(timer_sleep-0.005)
            time_cur = time.time_ns()

    @staticmethod
    def __show_img(wind, data, res):
        if wind.show_all_data:
            DataController.show_all_emotion(wind, res.res_arr)
        pixmap, scale = DrawingHelper.from_arr_to_pixelmap(data, wind.height_p*0.8)

        painter = QPainter(pixmap)
        DrawingHelper.create_pen_n_font(painter)

        for i in range(len(res.position)):
            if len(res.position[i]) > 0:
                painter.drawRect(int(res.position[i][0] * scale), int(res.position[i][1] * scale),
                                            int(res.position[i][2] * scale), int(res.position[i][3] * scale))
                text = ResultData.find_max_em(res.res_arr[i])[0]
                text = text[0] + " " + str(text[1]) + "%"
                painter.drawText(int(res.position[i][0] * scale)-10, int(res.position[i][1] * scale)-10, text)
        painter.end()
        del painter

        wind.lbl_img.setPixmap(pixmap)
        wind.lbl_img.adjustSize()
        if DataController.data:
            pos = (wind.lbl_img.width() + wind.pos_start[0], wind.pos_start[1])
            wind.lbl_au.move(pos[0], pos[1])

        del pixmap

    @staticmethod
    def __show_video(wind, data, res_v, res_a, with_audio=True, lvl=1.0):
        ad = data.audioPart
        vd = data.photoPart
        th2 = threading.Thread(target=lambda w=wind, v=vd, r=res_v: DataController.__func_t(w, v, r))
        th2.start()
        pos2 = int(wind.height_p*0.8/len(vd[0].raw_data)*len(vd[0].raw_data[0]))
        pos2 = (pos2, wind.pos_start[1])
        th = threading.Thread(target=lambda w=wind, d=ad.raw_data, sr=ad.sr, r=res_a, p=pos2, lv=lvl:
                            DataController.__show_audio(w, d, sr, r, lv, p))
        if with_audio:
            th.start()
            th.join()
        th2.join()

    @staticmethod
    def __func_t(wind, vd, res_v):
        i = 0
        c_time = time.time_ns()
        while i < len(vd) and not DataController.interrupt:
            r = ResultData()
            for j in range(len(res_v.res_arr[i])):
                r.add_new_data(res_v.res_arr[i][j], res_v.position[i][j])
            DataController.__show_img(wind, vd[i].raw_data, r)
            i += 1
            t = max(0.005, ResultData.spf - max((time.time_ns() - c_time) / 1e9, 0.0))
            time.sleep(t-0.005)
            c_time = time.time_ns()

    @staticmethod
    def show_all_emotion(wind, data, is_audio=False):
        if len(data) == 0:
            return
        ans = []
        colors = ResultData.colors_V
        if is_audio:
            colors = ResultData.colors_A
        for el in data:
            tmp = []
            i = 0
            for k in el.keys():
                tmp.append(colors[i])
                for j in range(int(el[k] * 20)):
                    tmp.append(colors[i])
                i += 1
            ans.append(tmp)

        for n in range(len(ans)):
            for j in range(0, 2000 - len(ans[n])):
                ans[n].append([255, 255, 255])
            ans[n] = ans[n][0:2000]
        shape = (len(ans), 2000, 3)
        ans = np.array(ans)
        ans = ans.astype(np.int8)
        ans = ans.reshape(shape)
        px, _ = DrawingHelper.from_arr_to_pixelmap(ans, wind.height_p*0.045, width=wind.width_p)
        painter = QPainter(px)
        DrawingHelper.create_pen_n_font(painter)
        painter.end()
        del painter
        if is_audio:
            wind.lbl_px_a.setPixmap(px)
            wind.lbl_px_a.adjustSize()
        else:
            wind.lbl_px_i.setPixmap(px)
            wind.lbl_px_i.adjustSize()

        del px

