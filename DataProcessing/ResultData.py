import datetime
import operator

import numpy as np

from GUI.Language import LENG


class ResultData:
    part_len = 2.5
    spf = 1.0/20.0
    fps = 20.0

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
        print("WR")
        name = self.type+" "+str(self.start_time)+'.txt'
        name = name.replace('—', '_')
        name = name.replace(':', '_')
        with open(name, 'w') as f:
            if rt:
                sec = self.start_time
            else:
                if self.type == "AUDIO":
                    f.write(self.file_name + "\n")
                    f.write(str(self.start_time) + "\n")
                    for el in self.res_arr:
                        f.write("" + str(sec) + ":" + str(el) + "\n")
                        sec = sec + ResultData.part_len
                elif self.type == "IMG":
                    f.write(self.file_name + "\n")
                    f.write(str(self.start_time) + "\n")
                    for i in range(len(self.position)):
                        f.write("" + str(self.position[i]) + ":" + str(self.res_arr[i]) + "\n")
                elif self.type == "VID":
                    f.write(self.file_name + "\n")
                    f.write(str(self.start_time) + "\n")
                    self.__prepare_vid_output(f)

                else:
                    f.write(LENG.elem.SYSTEM_MESS_ERR[2])

    def __prepare_vid_output(self, file):
        c = 0
        co = 0
        max_c = int(ResultData.part_len/ResultData.spf)
        tmp_pos, tmp_res = [], []
        for i in range(len(self.res_arr)):
            tmp_pos.append(self.position[i])
            tmp_res.append(self.res_arr[i])
            c += 1
            if c >= max_c:
                file.write(str(co*ResultData.part_len) + "\n")
                pos_t, res_t = self.__calc_mean_arr(tmp_res, tmp_pos)
                file.write(str(pos_t) + ":" + str(res_t) + "\n")
                tmp_pos, tmp_res = [], []
                co += 1
                c = 0

    @staticmethod
    def __calc_mean_arr(res, pos):
        res_t = {}
        pos_t = []
        fr = True
        total_l = 0
        for i in res:
            total_l += len(i)
        for t in range(len(res)):
            res_in_f = res[t]
            pos_in_f = pos[t]
            if len(res_in_f) > 0:
                for h in range(len(res_in_f)):
                    if fr:
                        fr = False
                        for k in res_in_f[h].keys():
                            res_t[k] = np.around(res_in_f[h][k] / total_l, decimals=2)
                        pos_t = pos_in_f[h]
                        for k in range(len(pos_t)):
                            pos_t[k] = int(pos_t[k] / total_l)
                    else:
                        for k in res_in_f[h].keys():
                            res_t[k] += np.around(res_in_f[h][k] / total_l, decimals=2)
                        for k in range(len(pos_in_f[h])):
                            pos_t[k] += int(pos_in_f[h][k] / total_l)
        return pos_t, res_t
