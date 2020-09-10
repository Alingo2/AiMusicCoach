# -*- coding: utf-8 -*-
from pydub import AudioSegment  # 先导入这个模块
import librosa
import matplotlib.pyplot as plt
import librosa.display
import numpy as np
import math
import numpy.fft as nf
import scipy.io.wavfile as wf
import os
filepath0 = "./test/cool5.wav"
filename="./test/cool5_"

def fre_to_note(fre):
    index = round(math.log(fre / 82.4,2**(1/12)))
    dict = ["E2 ","F2 ","#F2 ","G2 ","#G2 ","A2 ","#A2 ","B2 ","C3 ","#C3 ","D3 ","#D3 ","E3 ","F3 ","#F3 ","G3 ","#G3 ","A3 ","#A3 ","B3 ","C4 ","#C4 ","D4 ","#D4 ","E4 ","F4 ","#F4 ","G4 ","#G4 ","A4 ", "#A4 ", "B4 ", "C5 ", "#C5 ", "D5 ", "#D5 ", "E5 "]
    return dict[index]
def judge(time_domain_freq,frequency_domain_freq):
    if 1.05>=time_domain_freq/frequency_domain_freq>=1/1.05:
        return True
    return False
def freq_cul(filepath,i):
    result = 0
    sameple_rate, sigs = wf.read(filepath + str(i) + ".wav")
    sigs = sigs / (2 ** 15)
    sigs = sigs[:2 * len(sigs) // 3]
    sigs = np.array(sigs)
    sigs = (sigs.T[0] + sigs.T[1]) / 2
    times = np.arange(len(sigs)) / sameple_rate

    freqs = nf.fftfreq(sigs.size, 1 / sameple_rate)
    complex_arry = nf.fft(sigs)
    pows = np.abs(complex_arry)
    max_pows_num=pows.argmax()
    fun_freq = abs(freqs[max_pows_num])
    max_pows=int(pows[max_pows_num])# 获取频率域中能量最高的

    bolt = sameple_rate
    mark1 = (sigs.size) // 3
    sigs0 = sigs[mark1:mark1 + (bolt // 80) * 6]
    corre = librosa.core.autocorrelate(sigs0)
    corre1 = corre[bolt // 1100:bolt // 80]
    per = np.argmax(corre1) + bolt // 1100

    Tdomain_freq=bolt / per
    if not judge(Tdomain_freq,fun_freq):
        print(i)
        distant=freqs[1]-freqs[0]
        tdo_num=int(Tdomain_freq//distant)
        #print(tdo_num)
        # print(pows[tdo_num-1:tdo_num+1])
        Tfreq_pow=max(pows[tdo_num-2:tdo_num+2])
        print("max_pow",Tdomain_freq)
        print("freqpow",fun_freq)
        distinguishment = Tfreq_pow/max_pows
        print(distinguishment)
        if distinguishment>0.1:
            result = Tdomain_freq
        else:
            result =fun_freq
    else:
        result=(Tdomain_freq+fun_freq)/2
        #print("比例：",distinguishment)
    return result
def cut_beat_pitch_detect(filepath,total_num):
    pitch_array=[]
    pitch_array1=[]
    for i in range(1,total_num+1):
        data=freq_cul(filepath,i)
        pitch_array.append(data)

    return pitch_array
def beat_cul(filepath):
    sr0=30000
    y, sr = librosa.load(filepath,sr=sr0)
    ratio = 512/sr0
    onsets_frames = librosa.onset.onset_detect(y,sr=sr0,units="frames")
    return onsets_frames*ratio
input_music = AudioSegment.from_wav(filepath0)
beat_time = beat_cul(filepath0)
b0=beat_time[:-1]
b1=beat_time[1:]
beat_duration=np.array(b1)-np.array(b0)
beat=80
music_beat=beat_duration*beat/60
music_beat=[round(i,2) for i in music_beat]
print(music_beat)
pre_time=0
for i in range(len(beat_time)-1):
    (input_music[beat_time[i]*1000:beat_time[i+1]*1000]).export(filename+str(i+1)+".wav", format="wav")# 截取音频的前3秒(单位为毫秒)
    # print(beat_time[i]*1000,beat_time[i+1]*1000)
    # output_music.export("./test/BC_"+str(i+1)+".wav", format="wav") # 保存音频，前面为保存的路径，后面为保存的格式
output_music0 = input_music[beat_time[-1]*1000:beat_time[-1]*1000+500] # 截取音频的前3秒(单位为毫秒)
output_music0.export(filename+str(len(beat_time))+".wav", format="wav") # 保存音频，前面为保存的路径，后面为保存的格式
result=cut_beat_pitch_detect(filename,len(beat_time))
print(result)
notes = "".join(fre_to_note(i) for i in result)
print(notes)
# print(result[1])
# print(judge(1.05,1))9