# -*- coding: utf-8 -*-
from pydub import AudioSegment  # 先导入这个模块
input_music = AudioSegment.from_wav("./test/guitar.wav")
output_music = input_music[4556.8:4693.33333333] # 截取音频的前3秒(单位为毫秒)
output_music.export("./test/p5.wav", format="wav") # 保存音频，前面为保存的路径，后面为保存的格式