#导入转换文件格式
from pydub import AudioSegment
song = AudioSegment.from_mp3(r"D:\MyCode\MyPython\AiMusicCoach\test\guitar.mp3")
song.export("./test/now.wav", format="wav")