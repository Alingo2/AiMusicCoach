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

# def period(a):
#     per = 0
#     length_voice=len(a)
#     R=[]
#     temp=0
#     for i in range (180,790): #i是自相关差
#         temp=0
#         for j in range(1,length_voice-i):
#             temp=temp+a[j]*a[j+i]
#         R.append(temp)
#     r = np.array(R)
#     print(r)
#     per = np.argmax(r)+180
#     return per


#读取音频文件,将其按照采样率离散化，返回采样率和信号
#sample_reate:采样率(每秒采样个数),　sigs:每个采样位移值。
#================1.原始音频信号,时域信息=================================
<<<<<<< HEAD
sameple_rate,sigs = wf.read('./test/dataset/out/guitar_acoustic_013-058-127_.wav')
=======
sameple_rate,sigs = wf.read('./test/pitch50.wav')
>>>>>>> 042930c360124f4d378aec70a288a5f5c60533e5
bolt = sameple_rate
print('采样率:{}'.format(sameple_rate))
print('信号点数量:{}'.format(sigs.size))
sigs = sigs/(2**15)
<<<<<<< HEAD
print("~~~~~~~~~~~~~~~~~~~",np.argmax(sigs)/bolt)
sigs=sigs[:2*len(sigs)//3]
sigs = np.array(sigs)
=======
sigs=sigs[:2*len(sigs)//3]
sigs = np.array(sigs)
print("~~~~~~~~~~~~~~~~~~~",sigs)
>>>>>>> 042930c360124f4d378aec70a288a5f5c60533e5
# sigs = (sigs.T[0] + sigs.T[1])/2
# print("11111111111",sigs)

times = np.arange(len(sigs))/sameple_rate
plt.figure('Filter',facecolor='lightgray')
plt.subplot(221)
plt.title('Time Domain',fontsize=16)
plt.ylabel('Signal',fontsize=12)
plt.grid(linestyle=':')
num = (sigs.size-1)                                 #报错切成sigs.size-1
plt.plot(times[:num],sigs[:num],color='dodgerblue',label='Noised Signal')
plt.legend()

#==================2.转换为频率域信号===================================
#基于傅里叶变换，获取音频频域信息
#绘制音频频域的: 频域/能量图像
freqs = nf.fftfreq(sigs.size, 1/sameple_rate)       #报错切成sigs.size-1

complex_arry = nf.fft(sigs)
pows = np.abs(complex_arry)
plt.subplot(222)
plt.title('Frequence Domain',fontsize=16)
plt.ylabel('power',fontsize=12)
plt.grid(linestyle=':')
print("22222",freqs[-1])
plt.semilogy(freqs[freqs>0],pows[freqs>0],color='dodgerblue',label='Noised Freq')
plt.legend()

#==============第3步=================================================
#将低能噪声去除后绘制音频频域的: 频率/能量图书
fun_freq = freqs[pows.argmax()] #获取频率域中能量最高的
print("主频率：   ",abs(fun_freq))
noised_idx_high = np.where(abs(freqs) >= 2000)[0] #获取所有噪声的下标
ca = complex_arry[:]
ca[noised_idx_high] = 1 #高通滤波      之后取对数为0
noised_idx_low = np.where(abs(freqs) <= 0)[0]
ca[noised_idx_low] = 1
# filter_pows = np.abs(complex_arry)
filter_pows = np.abs(ca)
db_to = np.log10(filter_pows)
# print("db_to:",db_to)
nor_max = db_to[np.argmax(db_to)]
normalization = db_to/nor_max
#print(len(normalization),len(filter_pows))
onset_peak = librosa.util.peak_pick(normalization[freqs>0],3, 3, 3, 3, 0.12, 5)
#print(freqs[onset_peak+1])
plt.subplot(224)
plt.ylabel('power',fontsize=12)
plt.grid(linestyle=':')
# plt.semilogy(freqs[freqs>0],filter_pows[freqs>0],color='dodgerblue',label='Filter Freq')
# plt.vlines(onset_peak, 0, 1000, colors = "r", linestyles = "dashed")
plt.plot(freqs[freqs>0],normalization[freqs>0],color='dodgerblue',label='Filter Signal')
plt.legend()
plt.vlines(freqs[onset_peak+1], 0, 1.5, colors = "r", linestyles = "dashed")
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
# s1 = np.array(sigs)
mark1 = (sigs.size)//3
sigs0 = sigs[mark1:mark1+(bolt//80)*6]
# sigs0 = sigs
print("sigs0:~~~~~~~~~~~~~~",len(sigs0))

s2 = np.array(filter_sigs)
mark2 = (sigs.size)//3
sigs1 = sigs[mark2:mark2+(bolt//80)*6]


#重新生成音频文件
filter_sigs = (filter_sigs*(2**15)).astype('i2')
# wf.write(r'denoise6.wav',sameple_rate,filter_sigs)

plt.tight_layout()
plt.show()


tic = timer()
corre = librosa.core.autocorrelate(sigs0)
print("bolt//1100:bolt//80",bolt//1100,bolt//80)
print(len(corre))
corre1=corre[bolt//1100:bolt//80]
per = np.argmax(corre1)+bolt//1100
print("per:",per)
toc = timer()
print("时间2：",toc - tic) # 输出的时间，秒为单位

corre = librosa.core.autocorrelate(sigs1)
corre1=corre[bolt//1100:bolt//80]
per2 = np.argmax(corre1)+bolt//1100

# print("频率:",frequence)
print("频率1:",bolt/per,"         频率2：",bolt/per2)
