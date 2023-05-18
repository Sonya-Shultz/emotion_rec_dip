from keras.models import load_model
import numpy as np


class CNN:
    emotionsAudio = ['Neutral', 'Calm', 'Happy', 'Sad', 'Angry', 'Fear', 'Disgust', 'Surprise']
    emotionsImg = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    img_model = None
    audio_model = None

    @staticmethod
    def __init__(a_file_name="./cnn_data/AudioModel.h5",
                 ph_file_name="./cnn_data/PhotoModel.h5"):
        CNN.audio_model = load_model(a_file_name)
        CNN.img_model = load_model(ph_file_name)

    @staticmethod
    def __set_to_emotions(data, isAudio=True):
        if data is None:
            return None
        res = {}
        em = CNN.emotionsAudio
        if not isAudio:
            em = CNN.emotionsImg
        sum_d = np.sum(data[0])
        for i in range(len(data[0])):
            pr = np.around(data[0][i]/sum_d*100, decimals=2)
            res[em[i]] = pr
        return res

    @staticmethod
    def predict_audio_data(data):
        try:
            res = CNN.audio_model.predict(np.array([data]))
        except Exception as e:
            print(e)
            res = None
        return CNN.__set_to_emotions(res)

    @staticmethod
    def predict_img_data(data):
        try:
            res = CNN.img_model.predict(np.array([data]))
        except Exception as e:
            print(e)
            return None
        return CNN.__set_to_emotions(res, isAudio=False)
