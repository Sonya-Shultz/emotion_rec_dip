import moviepy.editor as mp
from DataProcessing.ImgData import ImgData
from DataProcessing.AudioData import AudioData


class VideoData:
    def __init__(self):
        self.filename = ""
        self.audioPart = None
        self.photoPart = []
        self.fps = 1.0/30.0

    def read_file(self, filename):
        self.filename = filename
        self.audioPart = AudioData()
        self.photoPart = []
        video = mp.VideoFileClip(self.filename)
        video.audio.write_audiofile(r"tmp.mp3")
        self.audioPart.read_file("./tmp.mp3")
        for i in range(int(video.duration/2.5)+1):
            cl = video.subclip(i*2.5, min([((i+1)*2.5), video.duration]))
            for j in range(0, int(cl.duration / self.fps)+1):
                cl2 = cl.subclip(j * self.fps, (j+1) * self.fps)
                imd = ImgData()
                imd.set_raw_data(cl2.get_frame(0))
                self.photoPart.append(imd)
