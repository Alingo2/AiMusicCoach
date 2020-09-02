# -*- coding: utf-8 -*-
from pydub import AudioSegment  # 先导入这个模块
input_music = AudioSegment.from_wav(r"D:\guitar_coach\3.wav")
output_music = input_music[2000:4000] # 截取音频的前3秒(单位为毫秒)
output_music.export(r"D:\guitar_coach\new1.wav", format="wav") # 保存音频，前面为保存的路径，后面为保存的格式