import wave
import matplotlib.pyplot as plt
import numpy as np
import os
 
filename = r"C:\Users\MSI-PC\Desktop\video\1.wav" #添加路径
f = wave.open(filename,'rb')
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
strData = f.readframes(nframes)#读取音频，字符串格式
waveData = np.fromstring(strData,dtype=np.int16)#将字符串转化为int
waveData = waveData*1.0/(max(abs(waveData)))#wave幅值归一化
# plot the wave
time = np.arange(0,nframes)*(1.0 / framerate)
plt.plot(time,waveData)
plt.xlabel("Time(s)")
plt.ylabel("Amplitude")
plt.title("Single channel wavedata")
plt.grid('on')#标尺，on：有，off:无。
plt.show()