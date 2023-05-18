import datetime
import numpy as np


class ResultData:

    __emotionsAudio = ['Neutral', 'Calm', 'Happy', 'Sad', 'Angry', 'Fear', 'Disgust', 'Surprise']
    __emotionsImg = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    file_name = ""
    type = ""
    res_arr = []
    start_time = None

    def set_param(self, fn, typ):
        self.file_name = fn
        self.type = typ
        self.start_time = datetime.datetime.now()

    def add_new_data(self, data):
        self.res_arr.append(data)

    @staticmethod
    def set_to_emotions(data, is_audio=True):
        if data is None:
            return None
        res = {}
        em = ResultData.__emotionsAudio
        if not is_audio:
            em = ResultData.__emotionsImg
        sum_d = np.sum(data[0])
        for i in range(len(data[0])):
            pr = np.around(data[0][i] / sum_d * 100, decimals=2)
            res[em[i]] = pr
        return res

