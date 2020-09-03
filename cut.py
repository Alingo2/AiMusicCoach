# -*- coding: utf-8 -*-
from pydub import AudioSegment  # 先导入这个模块
input_music = AudioSegment.from_wav("./test/A3CE4.wav")
output_music = input_music[1500:] # 截取音频的前3秒(单位为毫秒)
output_music.export("./test/partE4.wav", format="wav") # 保存音频，前面为保存的路径，后面为保存的格式