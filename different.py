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
import json

def fre_to_note(fre):
    index = round(math.log(fre / 82.4,2**(1/12)))
    dict = ["E2 ","F2 ","#F2 ","G2 ","#G2 ","A2 ","#A2 ","B2 ","C3 ","#C3 ","D3 ","#D3 ","E3 ","F3 ","#F3 ","G3 ","#G3 ","A3 ","#A3 ","B3 ","C4 ","#C4 ","D4 ","#D4 ","E4 ","F4 ","#F4 ","G4 ","#G4 ","A4 ", "#A4 ", "B4 ", "C5 ", "#C5 ", "D5 ", "#D5 ", "E5 "]
    return dict[index]

def fre_to_note_piano(fre):
    index = round(math.log(fre / 27.5,2**(1/12)))
    dict = ["A1 ","#A1 ","B1 ","C2 ","#C2 ","D2 ","#D2 ","E2 ","F2 ","#F2 ","G2 ","#G2 ","A2 ","#A2 ","B2 ","C3 ","#C3 ","D3 ","#D3 ","E3 ","F3 ","#F3 ","G3 ","#G3 ","A3 ","#A3 ","B3 ","C4 ","#C4 ","D4 ","#D4 ","E4 ","F4 ","#F4 ","G4 ","#G4 ","A4 ", "#A4 ", "B4 ", "C5 ", "#C5 ", "D5 ", "#D5 ", "E5 ","F5 ","#F5 ","G5 ","#G5 ","A5 ", "#A5 ", "B5 ", "C6 ", "#C6 ", "D6 ", "#D6 ", "E6 ",
    "F6 ","#F6 ","G6 ","#G6 ","A6 ", "#A6 ", "B6 ", "C7 ", "#C7 ", "D7 ", "#D7 ", "E7 ","F7 ","#F7 ","G7 ","#G7 ","A7 ", "#A7 ", "B7 ", "C8 ","#C8 ","D8 ","#D8 ","E8 ","F8 ","#F8 ","G8 ","#G8 ","A8 ","#A8 ","B8 ","C9"]
    return dict[index],index+21


def judge(time_domain_freq,frequency_domain_freq):
    if frequency_domain_freq == 0:
        return False
    if 1.05>=time_domain_freq/frequency_domain_freq>=1/1.05:
        return True
    return False
def freq_cul(filepath):
    num0=0
    result = 0
    sameple_rate, sigs = wf.read(filepath+ ".wav")
    sigs = sigs / (2 ** 15)
    sigs = sigs[:2 * len(sigs) // 3]              #使泛音衰减
    # sigs = sigs[2 * len(sigs) // 3:] 
    sigs = np.array(sigs)
    # sigs = (sigs.T[0] + sigs.T[1]) / 2            #双声道转换
    times = np.arange(len(sigs)) / sameple_rate

    freqs = nf.fftfreq(sigs.size, 1 / sameple_rate)
    complex_arry = nf.fft(sigs)
    pows = np.abs(complex_arry)
    max_pows_num=pows.argmax()
    fun_freq = abs(freqs[max_pows_num])
    max_pows=int(pows[max_pows_num])# 获取频率域中能量最高的

    bolt = sameple_rate
    # mark1 = 0
    # sigs0 = sigs
    mark1 = (sigs.size) // 3
    sigs0 = sigs[mark1:mark1 + (bolt // 80) * 6]
    corre = librosa.core.autocorrelate(sigs0)
    corre1 = corre[bolt // 1100:bolt // 80]
    per = np.argmax(corre1) + bolt // 1100

    Tdomain_freq=bolt / per
    if not judge(Tdomain_freq,fun_freq):
        num0=1
        distant=freqs[1]-freqs[0]
        tdo_num=int(Tdomain_freq//distant)
        Tfreq_pow=max(pows[tdo_num-2:tdo_num+2])
        distinguishment = Tfreq_pow/max_pows
        if distinguishment>0.1:
            result = Tdomain_freq
        else:
            result =fun_freq
    else:
        result=(Tdomain_freq+fun_freq)/2
    return [num0,filepath]

def cut(filepath):
    y, sr = librosa.load(filepath,sr=sr0)
    onsets_frames = (librosa.onset.onset_detect(y,sr=sr0,units="frames"))*ratio
    if len(onsets_frames)>0:
        return True,onsets_frames[0]
    else:
        return False,0
obj_r=open("./test/json/examples1.json")
data=json.load(obj_r)
guitar_data=[]
for file_data in data.items():
    if file_data[1]['instrument_family']==3 and file_data[1]["instrument_source_str"]=="acoustic":
        guitar_data.append([file_data[1]['note_str'],file_data[1]['pitch']])

sr0 = 30000
ratio = 512/sr0
num = 0
num1=0
right_num = 0
wrong = []
zero = []
strange =[]
file_list=[]
for i in range(len(guitar_data)):
    # filepath = "./test/dataset/" + guitar_data[i][0] + ".wav"
    filename = "./test/dataset/out/" + guitar_data[i][0] + "_"
    # input_music = AudioSegment.from_wav(filepath)
    # output_music0 = input_music[:1500]
    # flag,start = cut(filepath)
    # if flag:
    #     output_music0 = input_music[start*1000:start*1000+1000]
    # else:
    #     output_music0 = input_music[:500]
    #     strange.append(guitar_data[i][0])
    # output_music0.export(filename+".wav", format="wav") # 保存音频，前面为保存的路径，后面为保存的格式
    result=freq_cul(filename)
    # print(result)
    if 40<=guitar_data[i][1]<=84:
        num += 1
        if result[0] == 0:
            num1+=1
            zero.append(guitar_data[i][0])
            continue
        else:
            file_list.append(result[1])
        notes = fre_to_note_piano(result[0])
        if guitar_data[i][1] == notes[1]:
            right_num += 1
        else:
            print(guitar_data[i][1],notes[1])
            wrong.append(guitar_data[i][0])
accrucy = right_num/num
print("总数:",num)
print(num1)
print("accrucy:",accrucy)
print("错误数量：",len(wrong))
print(wrong)
print("为0数量：",len(zero))
print(zero)
print("音频长度检测错误数量：",len(strange))
print(strange)
with open("filename_list.txt","w") as f:
    f.write(str(file_list))