# -*- coding: utf-8 -*-
from pydub import AudioSegment  # 先导入这个模块
import librosa
import matplotlib.pyplot as plt
import librosa.display
import numpy as np
import numpy.fft as nf
import scipy.io.wavfile as wf
import os
filepath0 = "./test/cool2.wav"
filename="./test/cool2_"
def judge(time_domain_freq,frequency_domain_freq):
    if 1.05>=time_domain_freq/frequency_domain_freq>=1/1.05:
        return True
    return False

def cut_beat_pitch_detect(filepath,total_num):
    pitch_array=[]
    pitch_array1=[]
    for i in range(1,total_num+1):
        sameple_rate, sigs = wf.read(filepath+str(i)+".wav")
        sigs = sigs / (2 ** 15)
        sigs = np.array(sigs)
        sigs = (sigs.T[0] + sigs.T[1]) / 2
        times = np.arange(len(sigs)) / sameple_rate

        bolt = sameple_rate
        mark1 = (sigs.size) // 3 * 2
        sigs0 = sigs[:mark1]
        corre = librosa.core.autocorrelate(sigs0)
        corre1 = corre[bolt // 1100:bolt // 80]
        per = np.argmax(corre1) + bolt // 1100
        print(per)
        pitch_array.append(bolt/per)
        freqs = nf.fftfreq(sigs0.size, 1 / sameple_rate)
        complex_arry = nf.fft(sigs0)
        pows = np.abs(complex_arry)
        fun_freq = freqs[pows.argmax()]  # 获取频率域中能量最高的
        pitch_array1.append(fun_freq)

    return pitch_array,pitch_array1
def beat_cul(filepath):
    sr0=30000
    y, sr = librosa.load(filepath,sr=sr0)
    ratio = 512/sr0
    onsets_frames = librosa.onset.onset_detect(y,sr=sr0,units="frames")
    return onsets_frames*ratio
input_music = AudioSegment.from_wav(filepath0)
beat_time = beat_cul(filepath0)
pre_time=0
for i in range(len(beat_time)-1):
    (input_music[beat_time[i]*1000:beat_time[i+1]*1000]).export(filename+str(i+1)+".wav", format="wav")# 截取音频的前3秒(单位为毫秒)
    # print(beat_time[i]*1000,beat_time[i+1]*1000)
    # output_music.export("./test/BC_"+str(i+1)+".wav", format="wav") # 保存音频，前面为保存的路径，后面为保存的格式
output_music0 = input_music[beat_time[-1]*1000:] # 截取音频的前3秒(单位为毫秒)
output_music0.export(filename+str(len(beat_time))+".wav", format="wav") # 保存音频，前面为保存的路径，后面为保存的格式
result=cut_beat_pitch_detect(filename,len(beat_time))
print(result[0])
print(result[1])
print(judge(1.05,1))


