import numpy as np
import numpy.fft as nf
import scipy.io.wavfile as wf
import os
import librosa
from timeit import default_timer as timer
import json
obj_r=open("./test/json/examples3.json")
data=json.load(obj_r)
# obj1=open("./filename_list.json")
# data1=json.load(obj1)
guitar_data=[]
for file_data in data.items():
    if file_data[1]['instrument_family']==3 and file_data[1]["instrument_source_str"]=="acoustic":
        if 40<=file_data[1]['pitch']<=84:
            guitar_data.append([file_data[1]['note_str'],file_data[1]['pitch']])
# guitar_data=data1
def get_peak_data(filepath):
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

    fun_freq = freqs[pows.argmax()] #获取频率域中能量最高的
    noised_idx_high = np.where(abs(freqs) >= 2000)[0] #获取所有噪声的下标
    ca = complex_arry[:]
    ca[noised_idx_high] = 1 #高通滤波      之后取对数为0
    noised_idx_low = np.where(abs(freqs) <= 0)[0]
    ca[noised_idx_low] = 1
    # filter_pows = np.abs(complex_arry)
    filter_pows = np.abs(ca)
    db_to = np.log10(filter_pows)
    # print("db_to:",db_to)
    nor_max1 = filter_pows[np.argmax(filter_pows)]
    nor_max = db_to[np.argmax(db_to)]
    if nor_max==0:
        return 0
    normalization = db_to/nor_max
    normalization1 = filter_pows/nor_max1           ##nor_max1
    freq_data=normalization1[0:800]
    return freq_data
    # print(normalization)
    # if nor_max==0:
    #     print(filepath)
    # #print(len(normalization),len(filter_pows))
    # onset_peak = librosa.util.peak_pick(normalization[freqs>0],3, 3, 3, 3, 0.12, 5)
    # #print(freqs[onset_peak+1])    return [peak_freq,peak_pow,]
    # onset_peak=onset_peak.tolist()
    # if len(onset_peak)>10:
    #     onset_peak=onset_peak[:10]
    # elif len(onset_peak)>0 and len(onset_peak)<=10:
    #     for i in range(0,10-len(onset_peak)):
    #         onset_peak.append(0)
    # peak_freq=[]
    # # print(onset_peak)
    # peak_pow=[]
    # onset_peak=np.array(onset_peak)
    # if len(onset_peak) != 0:
    #     #print(onset_peak)
    #     peak_freq = onset_peak * (freqs[1] - freqs[0])
    #     for each_freq in onset_peak:
    #         if each_freq!=0:
    #             peak_pow.append(normalization1[each_freq+1])
    #         else:
    #             peak_pow.append(0)
    # # print(peak_freq)
    # # print(peak_pow)
    # #peak_pow=peak_pow
    #     for ii in range(0,10):
    #         result.append([peak_freq[ii]/1046.502/2,peak_pow[ii]])
    # #print(result)
    #     return result
    # else:
    #     return

result=[]
result1=[[],[]]
result2=[]
standard_pitch=[]
name=[]
for info in guitar_data:
    filepath='./test/dataset/out/'+info[0]+'_.wav'
    peakdata=get_peak_data(filepath)
    #print(peakdata)
    if peakdata != []:
        # print('0', peakdata)
        # print('1', peakdata[0])
        # result.append([info[0],info[1],peakdata[0],peakdata[1]])
        # result1[0].append(peakdata[0])
        # result1[1].append(peakdaeta[1])

        result2.append(peakdata.tolist())
        standard_pitch.append((27.5*2**((info[1]-21)/12))/1046.502/2)
        #name.append(info[0])
#result1 = np.array(result1)
#result2 = np.array(result2)
print(len(result2))
# result2=result2.tolist()
# standard_pitch=standard_pitch.tolist()
with open("datasetx_train3.json","w") as f:
        json.dump(result2,f)
with open("datasetx_result3.json","w") as f:
        json.dump(standard_pitch,f)