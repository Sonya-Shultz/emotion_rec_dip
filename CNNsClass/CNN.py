from keras.models import load_model
import numpy as np
from joblib import load

from DataProcessing.ResultData import ResultData


class CNN:
    scaler = None
    img_model = None
    audio_model = None

    @staticmethod
    def __init__(a_file_name="./cnn_data/AudioModel.h5",
                 ph_file_name="./cnn_data/PhotoModel.h5"):
        CNN.audio_model = load_model(a_file_name)
        CNN.img_model = load_model(ph_file_name)
        CNN.scaler = load('./cnn_data/std_scaler.bin')

    @staticmethod
    def predict_audio_data(data):
        try:
            res = CNN.audio_model.predict(np.array([data]), verbose=0)
        except Exception as e:
            return None
        return ResultData.set_to_emotions(res)

    @staticmethod
    def predict_img_data(data):
        try:
            res = CNN.img_model.predict(np.array([data]), verbose=0)
        except Exception as e:
            return None
        return ResultData.set_to_emotions(res, is_audio=False)
