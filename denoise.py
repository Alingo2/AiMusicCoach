'''
基于傅里叶变换的频域滤波。
'''
import numpy as np
import numpy.fft as nf
import matplotlib.pyplot as plt
import scipy.io.wavfile as wf

#读取音频文件,将其按照采样率离散化，返回采样率和信号
#sample_reate:采样率(每秒采样个数),　sigs:每个采样位移值。
#================1.原始音频信号,时域信息=================================
sameple_rate,sigs = wf.read(r'D:\guitar_coach\2.wav')
print('采样率:{}'.format(sameple_rate))
print('信号点数量:{}'.format(sigs.size))
sigs = sigs/(2**15)

times = np.arange(len(sigs))/sameple_rate
plt.figure('Filter',facecolor='lightgray')
plt.subplot(221)
plt.title('Time Domain',fontsize=16)
plt.ylabel('Signal',fontsize=12)
plt.grid(linestyle=':')
plt.plot(times[:178],sigs[:178],color='dodgerblue',label='Noised Signal')
plt.legend()

#==================2.转换为频率域信号===================================
#基于傅里叶变换，获取音频频域信息
#绘制音频频域的: 频域/能量图像
freqs = nf.fftfreq(sigs.size, 1/sameple_rate)
complex_arry = nf.fft(sigs)
pows = np.abs(complex_arry)
plt.subplot(222)
plt.title('Frequence Domain',fontsize=16)
plt.ylabel('power',fontsize=12)
plt.grid(linestyle=':')
plt.semilogy(freqs[freqs>0],pows[freqs>0],color='dodgerblue',label='Noised Freq')
plt.legend()

#==============第3步=================================================
#将低能噪声去除后绘制音频频域的: 频率/能量图书
fun_freq = freqs[pows.argmax()] #获取频率域中能量最高的
noised_idx = np.where(freqs != fun_freq)[0] #获取所有噪声的下标
ca = complex_arry[:]
ca[noised_idx] = 0 #高通滤波
filter_pows = np.abs(complex_arry)

plt.subplot(224)
plt.ylabel('power',fontsize=12)
plt.grid(linestyle=':')
plt.plot(freqs[freqs>0],filter_pows[freqs>0],color='dodgerblue',label='Filter Freq')
plt.legend()
#================第4步==============================================
filter_sigs = nf.ifft(ca)
plt.subplot(223)
plt.title('Time Domain',fontsize=16)
plt.ylabel('Signal',fontsize=12)
plt.grid(linestyle=':')
plt.plot(times[:178],filter_sigs[:178],color='dodgerblue',label='Filter Signal')
plt.legend()

#重新生成音频文件
filter_sigs = (filter_sigs*(2**15)).astype('i2')
wf.write(r'D:\guitar_coach\1.wav',sameple_rate,filter_sigs)

plt.tight_layout()
plt.show()