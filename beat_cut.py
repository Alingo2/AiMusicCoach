# -*- coding: utf-8 -*-
from pydub import AudioSegment  # 先导入这个模块
import librosa
import matplotlib.pyplot as plt
import librosa.display
import numpy as np
filepath0 = "./test/guitar2.wav"
def beat_cul(filepath):
    sr0=30000
    y, sr = librosa.load(filepath,sr=sr0)
    ratio = 512/sr0
    onsets_frames = librosa.onset.onset_detect(y,sr=sr0,units="frames")
    return onsets_frames*ratio
input_music = AudioSegment.from_wav(filepath0)
beat_time = beat_cul(filepath0)
print(beat_time*1000)
pre_time=0
for i in range(len(beat_time)-1):
    (input_music[beat_time[i]*1000:beat_time[i+1]*1000]).export("./test/BC2_"+str(i+1)+".wav", format="wav")# 截取音频的前3秒(单位为毫秒)
    # print(beat_time[i]*1000,beat_time[i+1]*1000)
    # output_music.export("./test/BC_"+str(i+1)+".wav", format="wav") # 保存音频，前面为保存的路径，后面为保存的格式
output_music0 = input_music[beat_time[-1]*1000:] # 截取音频的前3秒(单位为毫秒)
output_music0.export("./test/BC2_"+str(len(beat_time))+".wav", format="wav") # 保存音频，前面为保存的路径，后面为保存的格式