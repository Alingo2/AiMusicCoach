import numpy as np
import numpy.fft as nf
import scipy.io.wavfile as wf
import os
import librosa
from timeit import default_timer as timer
import json
obj_r=open("./test/json/examples3.json")
data=json.load(obj_r)
guitar_data=[]
#逐一导入音频文件
for file_data in data.items():
    if file_data[1]['instrument_family']==3 and file_data[1]["instrument_source_str"]=="acoustic":
        if 40<=file_data[1]['pitch']<=84:
            guitar_data.append([file_data[1]['note_str'],file_data[1]['pitch']])
#获取音频数据
def get_time_data(filepath):
    result=[]
    sameple_rate,sigs = wf.read(filepath)
    bolt = sameple_rate
    # print('采样率:{}'.format(sameple_rate))
    # print('信号点数量:{}'.format(sigs.size))
    sigs = sigs/(2**15)
    sigs=sigs[:2*len(sigs)//3]
    sigs = np.array(sigs)
    times = np.arange(len(sigs))/sameple_rate

    freqs = nf.fftfreq(sigs.size, 1/sameple_rate)       #报错切成sigs.size-1
    complex_arry = nf.fft(sigs)
    pows = np.abs(complex_arry)
    mark1 = (sigs.size) // 3
    sigs0 = sigs[mark1:mark1 + (bolt // 80) * 8]
    sigs0=abs(sigs0)
    sigs0=sigs0 / max(sigs0)
    sigs0=sigs0.tolist()
    return sigs0

result=[]
result1=[[],[]]
result2=[]
standard_pitch=[]
name=[]
#逐一对音频进行处理
for info in guitar_data:
    # filepath='./test/dataset/out'+info[0]+'_.wav'
    filepath='./test/dataset/out/'+info[0]+'_.wav'
    timedata=get_time_data(filepath)
    result2.append(timedata)
    standard_pitch.append((27.5 * 2 ** ((info[1] - 21) / 12)) / 1046.502 / 2)
#result1 = np.array(result1)
#result2 = np.array(result2)
with open("t_domain_data3.txt","w") as f:
    f.write(str(result2))
with open("t_domain_pitch3.txt","w") as f1:
    f1.write(str(standard_pitch))
# print(result2)
print(len(standard_pitch))