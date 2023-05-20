import operator
import cv2
import numpy as np
import threading
import pyaudio

from DataProcessing.AudioData import AudioData
from DataProcessing.ImgData import ImgData
from DataProcessing.VideoData import VideoData


class PrepareData:
    @staticmethod
    def for_audio(filename):
        ad = AudioData()
        ad.read_file(filename)
        res = ad.process()
        return ad, res

    @staticmethod
    def for_photo(filename):
        imd = ImgData()
        imd.read_file(filename)
        res = imd.process()
        return imd, res

    @staticmethod
    def __video_rl_part():
        cap = cv2.VideoCapture(0)

        while 1:
            ret, img = cap.read()
            imd = ImgData()
            imd.set_raw_data(img)
            res = imd.process()

            k = cv2.waitKey(30) & 0xff
            if k == 27:
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
            res = ad.process()

            k = cv2.waitKey(30) & 0xff
            if k == 27:
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
    def for_video(filename, with_sound=True, with_video=True):
        vd = VideoData()
        vd.read_file(filename)
        res1 = None
        if with_sound:
            res1 = vd.audioPart.process()
        res2 = []
        if with_video:
            for i in range(len(vd.photoPart)):
                el = vd.photoPart[i]
                res2.append(el.process())
        return vd, res1, res2

    @staticmethod
    def __find_max_em(data, em_numb=1):
        max_em = []
        if em_numb > len(data):
            em_numb = len(data)
        sorted_h = sorted(data.items(), key=operator.itemgetter(1))
        sorted_h.reverse()
        max_em.append(sorted_h[:em_numb])
        return max_em[0]


