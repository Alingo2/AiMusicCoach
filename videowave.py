import wave
import matplotlib.pyplot as plt
import numpy as np
import librosa
import os

filename= r"G:\guit\AiMusicCoach\test\changeC4C4C4G3E4E4E4C4.wav"
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
librosa.output.write_wav(output_filename,waveData,128000)
