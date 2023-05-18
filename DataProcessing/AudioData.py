import librosa
from librosa import load, feature
import numpy as np

from CNNsClass.CNN import CNN
from DataProcessing.ResultData import ResultData


class AudioData:

    def __init__(self):
        self.filename = ""
        self.raw_data = []
        self.features = []

    def read_file(self, filename):
        self.filename = filename
        self.raw_data, sr = load(self.filename)
        tmp_arr = self.__divide(sr)
        for el in tmp_arr:
            ele = AudioData.__find_features(el, sr)
            self.features.append(ele)

    def read_input(self, data, sr):
        self.raw_data = data
        tmp_arr = self.__divide(sr)
        for el in tmp_arr:
            ele = AudioData.__find_features(el, sr)
            self.features.append(ele)

    def __divide(self, sr):
        last_ind = 0
        tmp_arr = []
        len_in_chank = int(len(self.raw_data) / sr / ResultData.part_len)

        for i in range(0, len_in_chank):
            tmp_arr.append(self.raw_data[last_ind: int((i + 1) * sr * ResultData.part_len)])
            last_ind = int((i + 1) * sr * ResultData.part_len)
        tmp_arr.append(self.raw_data[last_ind: len(self.raw_data)])
        for i in range(0, len(tmp_arr[0]) - len(tmp_arr[len(tmp_arr) - 1])):
            np.append(tmp_arr[len(tmp_arr) - 1], 0)
        return tmp_arr

    @staticmethod
    def __find_features(data, sr):
        result = np.array([])
        ZeroCrossingRate = np.mean(feature.zero_crossing_rate(y=data).T, axis=0)
        result = np.hstack((result, ZeroCrossingRate))

        stft = np.abs(librosa.stft(data))
        chroma = np.mean(feature.chroma_stft(S=stft, sr=sr).T, axis=0)
        result = np.hstack((result, chroma))

        mfcc = np.mean(feature.mfcc(y=data, sr=sr).T, axis=0)
        result = np.hstack((result, mfcc))

        rootMeanSquare = np.mean(feature.rms(y=data).T, axis=0)
        result = np.hstack((result, rootMeanSquare))

        mSpect = np.mean(feature.melspectrogram(y=data, sr=sr).T, axis=0)
        result = np.hstack((result, mSpect))
        return result

    def process(self):
        data = self.features
        data = CNN.scaler.transform(data)
        data = np.expand_dims(data, axis=2)
        res = ResultData()
        res.set_param(self.filename, "AUDIO")
        for el in data:
            res.add_new_data(CNN.predict_audio_data(el))
        return res
