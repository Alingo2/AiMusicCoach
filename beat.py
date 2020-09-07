import librosa
import matplotlib.pyplot as plt
import librosa.display
import numpy as np
# # Load the signal
# x, sr = librosa.load('./test/A3CE4.wav',sr=None)
# zero_crossings = librosa.zero_crossings(x, pad=False)
# print(sum(zero_crossings))


sr0=30000
y, sr = librosa.load('./test/cool1.wav',sr=sr0)
ratio = 512/sr0
#print(sr)
# onset_env = librosa.onset.onset_strength(y=y, sr=128000,hop_length=512,aggregate=np.median)
onsets_frames = librosa.onset.onset_detect(y,sr=sr0,units="frames")
#print(onsets_frames/max(onsets_frames))
print(onsets_frames*ratio)
D = librosa.stft(y)
librosa.display.specshow(librosa.amplitude_to_db(D))
plt.vlines(onsets_frames, 0, sr, color='r', linestyle='--')
plt.show()

# librosa.util.peak_pick
# tempo, beats = librosa.beat.beat_track(y=y, sr=sr)


# mel = np.abs(librosa.feature.melspectrogram(y, fmax=11025))
# amp_db = librosa.power_to_db(mel)

# diff = np.maximum(amp_db[:,1:] - amp_db[:,:-1], 0.0)
# onset_amp = np.mean(diff, axis=0)
# onset_my = librosa.amplitude_to_db(onset_amp)

# onset_my -= onset_my.min()
# onset_my /= onset_my.max()
# onset_peak = librosa.util.peak_pick(onset_my,1, 1, 1, 1, 0.8, 5)