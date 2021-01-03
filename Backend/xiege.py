import numpy as np
from keras.models import load_model
import json
import copy
import play_music
import trans_music

# print(new_song)
#谱曲
def comp(y,model,model_2):
    print(y)
    x=np.array(y)
    temp1=np.argmax(model.predict(x)[0])/2
    temp2=(np.argmax(model_2.predict(x)[0])+1)/4
    #print([temp1,temp2])
    return [temp1,temp2]
#谱曲
def Compose(filename):
    UPLOAD_FOLDER = 'D:\MyCode\MyPython\AiMusicCoach\Backend'
    model = load_model(UPLOAD_FOLDER+"\composer.h5")
    model_2= load_model(UPLOAD_FOLDER+"\composer_2.h5")
    obj_r = open(UPLOAD_FOLDER + "\\"+filename)
    music = json.load(obj_r)
    y = music
    # new_song = [[0, 0.5], [5, 1], [9, 0.5], [5, 0.5], [0, 0.5], [2, 0.5], [9, 0.5], [5, 0.5],
    #         [0, 0.5], [2, 0.5], [9, 0.5], [5, 0.5], [2, 0.5], [9, 0.5], [2, 0.5], [6, 0.5],
    #         [5, 0.5], [9, 2], [5, 2], [3, 2]]
    new_song = copy.deepcopy(y[0])
    x = np.array(y)
    for i in range(50):
        new_note = comp(x,model,model_2)
        y[0].append(new_note)
        new_song.append(new_note)
        del(y[0][0])
        x = np.array(y)  
# print(new_song)
    with open("D:/MyCode/MyPython/AiMusicCoach/Backend/song/new_song.json","w") as f:
        json.dump(new_song,f)
    trans_music.transe(UPLOAD_FOLDER +"\\song\\new_song.json")
    play_music.play_Music(UPLOAD_FOLDER +"\\song\\mysong.json")
    return "new_song.json"

# Compose("wxa4d8c90caa7eb4f9.o6zAJsxvBGbHWnpJtSV_vgevLt5A.IsGAtqCBQ6LB2d1e1e56aa7dd0298759e35951677260.json")