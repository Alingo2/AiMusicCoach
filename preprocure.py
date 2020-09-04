import wave as we
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.signal import windows
 
# 分帧处理函数
def generate_frame_data(x, sr, win, overlap):
    n_frames = 1 + int(len(x) / overlap)
 
    y = np.zeros((win, n_frames))
    x = np.pad(x, (0, n_frames * overlap + win - len(x)), 'constant', constant_values=0)
 
    for n in range(n_frames):
        y[:, n] = x[n * overlap:n * overlap + win]
         
    time = np.arange(0, len(x)/sr,overlap/sr)
    return y,time

#自相关函数
def compute_acf(wave_data):
    auto_corr_funtion = []
    for item in wave_data:
        auto_corr_funtion.append(compute_frame_acf(item))
    return np.array(auto_corr_funtion)
 
# 计算帧能量
def compute_frame_ste(frame_data):
    short_time_energy = np.sum(frame_data * frame_data, axis=0)
    return short_time_energy[:-1]

# 计算分帧之后的结果最大值
def comput_T0_acf(auto_corr_function):
    T0 = np.argmax(auto_corr_function[:, 10:], axis=1)
    return T0

filename = './test/C3G3C4G3E4G3C4G3慢.wav'
WAVE = we.open(filename)
print('---------声音信息------------')
for item in enumerate(WAVE.getparams()):
    print(item)
a = WAVE.getparams().nframes    # 帧总数
f = WAVE.getparams().framerate  # 采样频率
sample_time = 1/f               # 采样点的时间间隔
time = a/f                      #声音信号的长度
sample_frequency, audio_sequence = wavfile.read(filename)
print(audio_sequence)           #声音信号每一帧的“大小”
x_seq = np.arange(0,time,sample_time)

plt.plot(x_seq,audio_sequence,'blue')
plt.xlabel("time (s)")
plt.show()
print()