'''
基于傅里叶变换的频域滤波。
'''
import numpy as np
import numpy.fft as nf
import matplotlib.pyplot as plt
import scipy.io.wavfile as wf
import os
import librosa
from timeit import default_timer as timer
path = os.getcwd()
def period(a):
    per = 0
    length_voice=len(a)
    R=[]
    temp=0
    for i in range (180,790): #i是自相关差
        temp=0
        for j in range(1,length_voice-i):
            temp=temp+a[j]*a[j+i]
        R.append(temp)
    r = np.array(R)
    print(r)
    per = np.argmax(r)+180
    return per


#读取音频文件,将其按照采样率离散化，返回采样率和信号
#sample_reate:采样率(每秒采样个数),　sigs:每个采样位移值。
#================1.原始音频信号,时域信息=================================
sameple_rate,sigs = wf.read('./test/BC_1.wav')
print('采样率:{}'.format(sameple_rate))
print('信号点数量:{}'.format(sigs.size))
sigs = sigs/(2**15)
times = np.arange(len(sigs))/sameple_rate
plt.figure('Filter',facecolor='lightgray')
plt.subplot(221)
plt.title('Time Domain',fontsize=16)
plt.ylabel('Signal',fontsize=12)
plt.grid(linestyle=':')
num = sigs.size-1
plt.plot(times[:num],sigs[:num],color='dodgerblue',label='Noised Signal')
plt.legend()

#==================2.转换为频率域信号===================================
#基于傅里叶变换，获取音频频域信息
#绘制音频频域的: 频域/能量图像
freqs = nf.fftfreq(sigs.size, 1/sameple_rate)
print(freqs)
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
#print(fun_freq)
noised_idx_high = np.where(abs(freqs) >= 2000)[0] #获取所有噪声的下标
ca = complex_arry[:]
ca[noised_idx_high] = 0 #高通滤波
noised_idx_low = np.where(abs(freqs) <= 0)[0]
ca[noised_idx_low] = 0
filter_pows = np.abs(complex_arry)

plt.subplot(224)
plt.ylabel('power',fontsize=12)
plt.grid(linestyle=':')
plt.semilogy(freqs[freqs>0],filter_pows[freqs>0],color='dodgerblue',label='Filter Freq')
plt.legend()
#================第4步==============================================
filter_sigs = nf.ifft(ca)
plt.subplot(223)
plt.title('Time Domain',fontsize=16)
plt.ylabel('Signal',fontsize=12)
plt.grid(linestyle=':')
plt.plot(times[:num],filter_sigs[:num],color='dodgerblue',label='Filter Signal')
plt.legend()

# sigs0 = sigs
# sigs1 = filter_sigs
s1 = np.array(sigs)
mark1 = np.argmax(s1)
sigs0 = sigs[mark1:mark1+10000]

s2 = np.array(filter_sigs)
mark2 = np.argmax(s2)
sigs1 = sigs[mark2:mark2+10000]


#重新生成音频文件
filter_sigs = (filter_sigs*(2**15)).astype('i2')
# wf.write(r'denoise6.wav',sameple_rate,filter_sigs)

plt.tight_layout()
plt.show()

np.set_printoptions(threshold=np.inf)



tic = timer()
corre = librosa.core.autocorrelate(sigs0)
corre1=corre[120:1580]
per = np.argmax(corre1)+120
toc = timer()
print("时间2：",toc - tic) # 输出的时间，秒为单位

corre = librosa.core.autocorrelate(sigs1)
corre1=corre[120:1580]
per2 = np.argmax(corre1)+120

# print("频率:",frequence)
print("频率1:",128000/per,"         频率2：",128000/per2)
