import threading

import moviepy.editor as mp
from DataProcessing.ImgData import ImgData
from DataProcessing.AudioData import AudioData
from DataProcessing.ResultData import ResultData


class VideoData:

    def __init__(self):
        self.filename = ""
        self.audioPart = None
        self.photoPart = []

    def read_file(self, filename):
        self.filename = filename
        self.audioPart = AudioData()
        self.photoPart = []
        video = mp.VideoFileClip(self.filename)
        video = video.set_fps(ResultData.fps)
        audio = video.audio.to_soundarray(fps=22050)
        audio = audio.sum(axis=1) / 2.0
        th = threading.Thread(target=lambda a=audio: self.audioPart.read_input(a, 22050))
        th.start()
        for el in video.iter_frames():
            imd = ImgData()
            imd.set_raw_data(el)
            self.photoPart.append(imd)
        th.join()
