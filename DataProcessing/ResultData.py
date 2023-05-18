import datetime
import numpy as np

from GUI.Language import LENG


class ResultData:
    part_len = 2.5
    spf = 1.0/30.0

    def __init__(self):
        self.file_name = ""
        self.type = ""
        self.res_arr = []
        self.start_time = None
        self.position = None  # xyhw

    def set_param(self, fn, typ):
        self.file_name = fn
        self.type = typ
        self.start_time = datetime.datetime.now()

    def add_new_data(self, data, position=None):
        self.res_arr.append(data)
        self.position.append(position)

    @staticmethod
    def set_to_emotions(data, is_audio=True):
        if data is None:
            return None
        res = {}
        em = LENG.elem.AUDIO_EM
        if not is_audio:
            em = LENG.elem.IMG_EM
        sum_d = np.sum(data[0])
        for i in range(len(data[0])):
            pr = np.around(data[0][i] / sum_d * 100, decimals=2)
            res[em[i]] = pr
        return res

    def write_to_file(self, rt=False):
        sec = 0.0
        if rt:
            sec = self.start_time
        if self.type == "au":
            print(self.file_name)
            print(self.start_time)
            for el in self.res_arr:
                print(sec, ":", el)
                sec = sec + ResultData.part_len
        else:
            print(self.file_name)
            print(self.start_time)
            for i in range(len(self.res_arr)):
                print(self.position[i], ":" ,self.res_arr[i])
