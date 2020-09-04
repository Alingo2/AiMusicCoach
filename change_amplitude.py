import wave
import matplotlib.pyplot as plt
import numpy as np
import librosa
import os

filename = r"./test/guitar.wav" #添加路径
f = wave.open(filename,'rb')
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
strData = f.readframes(nframes)#读取音频，字符串格式
waveData = np.fromstring(strData,dtype=np.int16)#将字符串转化为int
waveData = waveData*1.0/(max(abs(waveData)))#wave幅值归一化
# plot the wave
time = np.arange(0,nframes)*(1.0 / framerate)
judge_time=[]
L=len(waveData)
N=28220
k=L//N
for i in range(1,k+1):
    sum=0
    I=N*i
    for j in range(I-N,I):
        if(abs(waveData[j])>0.05):
            sum=sum+abs(waveData[j])
    average=sum/N
    judge_time.append(average)
    for j in range(I-N,I):
        waveData[j]=average
sum=0
for i in range(k*N,L):
    if (abs(waveData[i]) > 0.05):
        sum = sum + abs(waveData[j])
average=sum/(L-k*N)
judge_time.append(average)
for i in range(k*N,L):
    waveData[i]=average
print(judge_time)
change_L=len(judge_time)
cut_time=[]
for i in range(2,change_L-1):
    if judge_time[i]<=judge_time[i-1] and judge_time[i]<=judge_time[i+1]:
        cut_time.append(i)

cut_time_final=[]
sr=1411000
for i in range(0,len(cut_time)-1):
    if  cut_time[i] != cut_time[i+1]-1:
        cut_time_final.append(cut_time[i]*N/sr)
if cut_time[-1]==cut_time[-2]+1:
    cut_time_final.append(cut_time[-1]*N/sr)



print(len(cut_time_final))
print(cut_time)
print(cut_time_final)
plt.plot(time,waveData)
plt.xlabel("Time(s)")
plt.ylabel("Amplitude")
plt.title("Single channel wavedata")
plt.grid('on')#标尺，on：有，off:无。
plt.show()

