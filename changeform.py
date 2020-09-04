from pydub import AudioSegment
song = AudioSegment.from_mp3(r"D:\MyCode\MyPython\AiMusicCoach\test\C6.wav")
song.export("./test/now.wav", format="wav")