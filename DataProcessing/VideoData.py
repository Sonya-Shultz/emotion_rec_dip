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
        video.audio.write_audiofile(r"tmp.mp3", logger=None)
        self.audioPart.read_file("./tmp.mp3")
        for i in range(int(video.duration/ResultData.part_len)+1):
            cl = video.subclip(i*ResultData.part_len, min([((i+1)*ResultData.part_len), video.duration]))
            for j in range(0, int(cl.duration * ResultData.fps)+1):
                cl2 = cl.subclip(j * ResultData.spf, (j+1) * ResultData.spf)
                imd = ImgData()
                imd.set_raw_data(cl2.get_frame(0))
                self.photoPart.append(imd)
