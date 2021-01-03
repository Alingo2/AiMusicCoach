import numpy as np
import wave as we
import scipy.io.wavfile as wf
import json
import random
obj_r=open("./test/json/examples.json")
data=json.load(obj_r)
guitar_data={}
for i in range(40,85):
    guitar_data[str(i)]=[]
#逐一导入单音文件
for file_data in data.items():
    if file_data[1]['instrument_family']==3 and file_data[1]["instrument_source_str"]=="acoustic":
        if 40<=file_data[1]['pitch']<=84:
            #print(guitar_data)
            guitar_data[str(file_data[1]['pitch'])].append(file_data[1]['note_str'])
print(guitar_data)
#时域叠加生成和弦音频
def create(filepath1,filepath2,base):
    try:
        sameple_rate1, sigs1 = wf.read(filepath1)
        sameple_rate2, sigs2 = wf.read(filepath2)
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
        return 0
    else:
        sigs1=sigs1.tolist()
        sigs2=sigs2.tolist()
        for i in range(0,40):
            sigs1.append(0)
            sigs2.insert(0,0)
        sigs1=np.array(sigs1)
        sigs2 = np.array(sigs2)
        sig=(sigs1+sigs2)/2

        save_wav = sig.real.reshape((len(sig), 1)).T.astype(np.short)
        f = we.open("./test/dataset/chord/"+base+'.wav', "wb")
        # 配置声道数、量化位数和取样频率
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        # 将wav_data转换为二进制数据写入文件
        f.writeframes(save_wav.tostring())
        f.close()
        return 1
#
a=[]
for pitch0 in range(40,77):
    i=1
    for file1 in guitar_data[str(pitch0)]:
        for file2 in guitar_data[str(pitch0+7)]:
            filepath1="./test/dataset/out/"+file1+"_.wav"
            filepath2="./test/dataset/out/"+file2+"_.wav"
            if(create(filepath1,filepath2,str(pitch0)+"_"+str(i))==1):
                a.append([file1,file2,str(pitch0)+"_"+str(i),pitch0])
                i+=1
random.shuffle(a)
with open("new_chord_list.json",'w') as f:
    json.dump(a,f)