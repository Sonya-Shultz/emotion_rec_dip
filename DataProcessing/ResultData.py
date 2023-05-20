import datetime
import operator

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
        self.position = []  # xyhw

    def set_param(self, fn, typ):
        self.file_name = fn
        self.type = typ
        self.start_time = datetime.datetime.now()

    def add_new_data(self, data, position=None):
        self.res_arr.append(data)
        self.position.append(position)

    @staticmethod
    def find_max_em(data, em_numb=1):
        max_em = []
        if em_numb > len(data):
            em_numb = len(data)
        sorted_h = sorted(data.items(), key=operator.itemgetter(1))
        sorted_h.reverse()
        max_em.append(sorted_h[:em_numb])
        return max_em[0]

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
        else:
            if self.type == "AUDIO":
                print(self.file_name)
                print(self.start_time)
                for el in self.res_arr:
                    print(sec, ":", el)
                    sec = sec + ResultData.part_len
            elif self.type == "IMG":
                print(self.file_name)
                print(self.start_time)
                for i in range(len(self.position)):
                    print(self.position[i], ":", self.res_arr[i])
            elif self.type == "VID":
                print("vid")
                print(self.file_name)
                print(self.start_time)
                self.__prepare_vid_output()

            else:
                print(LENG.elem.SYSTEM_MESS_ERR[2])

    def __prepare_vid_output(self):
        c = 0
        max_c = int(ResultData.part_len/ResultData.spf)
        tmp_pos, tmp_res = [], []
        for i in range(len(self.res_arr)):
            tmp_pos.append(self.position[i])
            tmp_res.append(self.res_arr[i])
            c += 1
            if c >= max_c:
                print(i*ResultData.part_len)
                self.__calc_mean_arr(tmp_res, tmp_pos)
                tmp_pos, tmp_res = [], []
                c = 0

    @staticmethod
    def __calc_mean_arr(res, pos):
        t_res = res[0]
        t_pos = pos[0]
        for i in range(1, len(res)):
            t_res += res[i]
            t_pos += pos[i]
        t_res = t_res / float(len(res))
        t_pos = t_pos / float(len(res))
        for i in range(t_res):
            print(t_pos[i], ":", t_res[i])
