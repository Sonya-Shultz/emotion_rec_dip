from matplotlib import image
import cv2
import numpy as np

from CNNsClass.CNN import CNN
from DataProcessing.ResultData import ResultData


class ImgData:
    face_cascade = cv2.CascadeClassifier('./cnn_data/haarcascade_frontalface_default.xml')

    def __init__(self):
        self.filename = ""
        self.raw_data = []
        self.features = []

    def read_file(self, filename):
        self.filename = filename
        self.raw_data = image.imread(self.filename)
        self.features = self.__find_features()

    def set_raw_data(self, data):
        self.raw_data = data
        self.features = self.__find_features()

    def __find_features(self):
        gray = cv2.cvtColor(self.raw_data, cv2.COLOR_BGR2GRAY)
        faces = ImgData.face_cascade.detectMultiScale(gray, 1.3, 5)
        tmp_arr = []
        for (x, y, w, h) in faces:
            tmp = []
            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48))
            tmp.extend([x, y, w, h])
            tmp.extend(roi_gray)
            tmp_arr.append(tmp)
        return tmp_arr

    def process(self):
        res = ResultData()
        res.set_param(self.filename, "IMG")
        for el in self.features:
            tmp = CNN.predict_img_data(np.reshape(el[4:], (48, 48)))
            res.add_new_data(tmp, position=el[:4])
        return res
    
