import threading
import time

from DataProcessing.AudioData import AudioData
from DataProcessing.ImgData import ImgData
from DataProcessing.ResultData import ResultData
from DataProcessing.VideoData import VideoData


class PrepareData:
    audio_d = None
    video_d = None
    res_t = None

    time_total = 0
    time_proc = 0

    @staticmethod
    def for_audio(filename):
        ad = AudioData()
        ad.read_file(filename)
        t_ = time.time()
        res = ad.process()
        PrepareData.time_proc = time.time() - t_
        return ad, res

    @staticmethod
    def for_photo(filename):
        imd = ImgData()
        imd.read_file(filename)
        t_ = time.time()
        res = imd.process()
        PrepareData.time_proc = time.time() - t_
        return imd, res

    @staticmethod
    def for_photo_data(data):
        imd = ImgData()
        imd.set_raw_data(data)
        t_ = time.time()
        res = imd.process()
        PrepareData.time_proc = time.time() - t_
        return imd, res

    @staticmethod
    def for_audio_data(data, sr):
        ad = AudioData()
        ad.read_input(data, sr)
        t_ = time.time()
        res = ad.process()
        PrepareData.time_proc = time.time() - t_
        return ad, res

    @staticmethod
    def for_video(filename, with_sound=True, with_video=True):
        vd = VideoData()
        vd.read_file(filename)
        res1 = None
        th = None
        t_ = time.time()
        if with_sound:
            th = threading.Thread(target=lambda d=vd.audioPart: PrepareData.__hlp(d))
            th.start()
        res22 = None
        if with_video:
            res22 = ResultData()
            res22.set_param(filename, "VID")
            for i in range(len(vd.photoPart)):
                el = vd.photoPart[i]
                r = el.process()
                res22.add_new_data(r.res_arr, position=r.position)
        if with_sound:
            th.join()
            res1 = PrepareData.res_t
        PrepareData.time_proc = time.time()-t_
        return vd, res1, res22

    @staticmethod
    def __hlp(data):
        PrepareData.res_t = data.process()
