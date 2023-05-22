from DataProcessing.AudioData import AudioData
from DataProcessing.ImgData import ImgData
from DataProcessing.ResultData import ResultData
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
    def for_photo_data(data):
        imd = ImgData()
        imd.set_raw_data(data)
        res = imd.process()
        return imd, res

    @staticmethod
    def for_audio_data(data, sr):
        ad = AudioData()
        ad.read_input(data, sr)
        res = ad.process()
        return ad, res

    @staticmethod
    def for_video(filename, with_sound=True, with_video=True):
        vd = VideoData()
        vd.read_file(filename)
        res1 = None
        if with_sound:
            res1 = vd.audioPart.process()
        res22 = None
        #res2 = []
        if with_video:
            res22 = ResultData()
            res22.set_param(filename, "VID")
            for i in range(len(vd.photoPart)):
                el = vd.photoPart[i]
                r = el.process()
                res22.add_new_data(r.res_arr, position=r.position)
        return vd, res1, res22



