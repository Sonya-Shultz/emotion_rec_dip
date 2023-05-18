import sys

from CNNsClass.CNN import CNN
from DataProcessing.PrepareData import PrepareData

import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)


if __name__ == '__main__':
    CNN()
    #PrepareData.for_photo("test.jpg")
    #PrepareData.for_video_real_time()
    #PrepareData.for_audio("test.mp3")
    PrepareData.for_video("test.MP4")

