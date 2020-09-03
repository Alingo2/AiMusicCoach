import librosa
import matplotlib.pyplot as plt
import librosa.display
# # Load the signal
# x, sr = librosa.load('./test/A3CE4.wav',sr=None)
# zero_crossings = librosa.zero_crossings(x, pad=False)
# print(sum(zero_crossings))




y, sr = librosa.load('./test/C4C4C4G3E4E4E4C4.wav',sr=None)
onsets_frames = librosa.onset.onset_detect(y)
D = librosa.stft(y)
librosa.display.specshow(librosa.amplitude_to_db(D))
plt.vlines(onsets_frames, 0, sr, color='r', linestyle='--')
plt.show()