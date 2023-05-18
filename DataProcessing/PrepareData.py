import operator
import cv2
import numpy as np
import threading
import pyaudio
import time

from DataProcessing.AudioData import AudioData
from DataProcessing.ImgData import ImgData
from DataProcessing.VideoData import VideoData
from joblib import load
from CNNsClass.CNN import CNN


class PrepareData:
    @staticmethod
    def for_audio(filename):
        ad = AudioData()

        ad.read_file(filename)
        res = PrepareData.__audio_hlp(ad.features)
        return res

    @staticmethod
    def for_photo(filename):
        imd = ImgData()
        imd.read_file(filename)
        res = PrepareData.__foto_hlp(imd.features, imd.raw_data)
        cv2.imshow('img', imd.raw_data)
        while 1:
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
            if cv2.getWindowProperty('img', cv2.WND_PROP_VISIBLE) < 1:
                break

        cv2.destroyAllWindows()
        return res

    @staticmethod
    def __audio_hlp(features):
        data = features
        sc = load('./cnn_data/std_scaler.bin')
        data = sc.transform(data)
        data = np.expand_dims(data, axis=2)
        res = []
        for el in data:
            res.append(CNN.predict_audio_data(el))
        return res

    @staticmethod
    def __foto_hlp(features, raw_data):
        res = []
        for el in features:
            tmp = CNN.predict_img_data(np.reshape(el[4:], (48, 48)))
            res.append(tmp)
            text = PrepareData.__find_max_em(tmp)[0]
            text = text[0]+" "+str(text[1])+"%"
            [x, y, w, h] = el[:4]
            cv2.rectangle(raw_data, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.putText(raw_data, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (26, 26, 255), 2)
        return res

    @staticmethod
    def __video_rl_part():
        cap = cv2.VideoCapture(0)

        while 1:
            ret, img = cap.read()
            imd = ImgData()
            imd.set_raw_data(img)
            res = PrepareData.__foto_hlp(imd.features, imd.raw_data)
            cv2.imshow('veb', img)

            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
            if cv2.getWindowProperty('veb', cv2.WND_PROP_VISIBLE) < 1:
                break
        cap.release()

    @staticmethod
    def __audio_rl_part():
        CHUNK = 1024
        FORMAT = pyaudio.paFloat32
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 2.5

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        while 1:
            frames = []
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                tmp_data = np.fromstring(data, dtype=np.float32)
                frames.append(tmp_data)
            frames = np.hstack(frames)

            ad = AudioData()
            ad.read_input(frames, RATE)

            img = frames
            img = np.reshape(img, (214, 512))

            res = PrepareData.__audio_hlp(ad.features)
            text = PrepareData.__find_max_em(res[0])[0]
            text = text[0] + " " + str(text[1]) + "%"
            cv2.putText(img, text, (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (26, 26, 255), 2)

            cv2.imshow('web', img)

            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
            if cv2.getWindowProperty('web', cv2.WND_PROP_VISIBLE) < 1:
                break
        stream.stop_stream()
        stream.close()
        p.terminate()

    @staticmethod
    def for_video_real_time():
        video_thread = threading.Thread(target=PrepareData.__video_rl_part)
        audio_thread = threading.Thread(target=PrepareData.__audio_rl_part)

        video_thread.start()
        audio_thread.start()
        video_thread.join()
        audio_thread.join()

        cv2.destroyAllWindows()

    @staticmethod
    def for_video(filename):
        vd = VideoData()
        vd.read_file(filename)
        res1 = PrepareData.__audio_hlp(vd.audioPart.features)
        res2 = []
        for i in range(len(vd.photoPart)):
            el = vd.photoPart[i]
            res2.append(PrepareData.__foto_hlp(el.features, el.raw_data))
            img = np.array(el.raw_data)
            text = PrepareData.__find_max_em(res1[int(i/(30.0*2.5))])[0]
            text = text[0] + " " + str(text[1]) + "%"
            cv2.putText(img, text, (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (26, 26, 255), 2)
            cv2.imshow('vid', img)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
            if cv2.getWindowProperty('vid', cv2.WND_PROP_VISIBLE) < 1:
                break
        cv2.destroyAllWindows()


    @staticmethod
    def __find_max_em(data, em_numb=1):
        max_em = []
        if em_numb > len(data):
            em_numb = len(data)
        sorted_h = sorted(data.items(), key=operator.itemgetter(1))
        sorted_h.reverse()
        max_em.append(sorted_h[:em_numb])
        return max_em[0]


