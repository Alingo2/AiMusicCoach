from flask import Flask,request,send_from_directory
from keras.models import load_model
import json
import os
import numpy as np
import sys
import xiege
from xiege import Compose
import scipy.io.wavfile as wf
import numpy.fft as nf
import librosa
from timeit import default_timer as timer
import beat_cut
import math

sys.path.append(os.path.dirname(__file__) + os.sep + '../')

UPLOAD_FOLDER = 'D:\MyCode\MyPython\AiMusicCoach\Backend'
app = Flask(__name__, static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024 #上传文件限制为最大 64 MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model_single = load_model(UPLOAD_FOLDER + "\CNN.h5")
model_hexian = load_model(UPLOAD_FOLDER+"\hexianclassification.h5")
model_fenlei = load_model(UPLOAD_FOLDER+"\mistake_classification.h5")
#音频转换
def index_to_note_piano(index):
    dict = ["A1 ","#A1 ","B1 ","C2 ","#C2 ","D2 ","#D2 ","E2 ","F2 ","#F2 ","G2 ","#G2 ","A2 ","#A2 ","B2 ","C3 ","#C3 ","D3 ","#D3 ","E3 ","F3 ","#F3 ","G3 ","#G3 ","A3 ","#A3 ","B3 ","C4 ","#C4 ","D4 ","#D4 ","E4 ","F4 ","#F4 ","G4 ","#G4 ","A4 ", "#A4 ", "B4 ", "C5 ", "#C5 ", "D5 ", "#D5 ", "E5 ","F5 ","#F5 ","G5 ","#G5 ","A5 ", "#A5 ", "B5 ", "C6 ", "#C6 ", "D6 ", "#D6 ", "E6 ",
    "F6 ","#F6 ","G6 ","#G6 ","A6 ", "#A6 ", "B6 ", "C7 ", "#C7 ", "D7 ", "#D7 ", "E7 ","F7 ","#F7 ","G7 ","#G7 ","A7 ", "#A7 ", "B7 ", "C8 ","#C8 ","D8 ","#D8 ","E8 ","F8 ","#F8 ","G8 ","#G8 ","A8 ","#A8 ","B8 ","C9 ","#C9 ", "D9 ", "#D9 ", "E9 ","F9 ","#F9 ","G9 ","#G9 ","A9 ", "#A9 ", "B9 ", "C10 "]
    return dict[index]
#文件分析
def get_peak_data(filepath,num):
    result=[]
    sameple_rate,sigs = wf.read(filepath)

    bolt = sameple_rate
    # print('采样率:{}'.format(sameple_rate))
    # print('信号点数量:{}'.format(sigs.size))
    sigs = sigs/(2**15)
    sigs=sigs[:2*len(sigs)//3]
    sigs = np.array(sigs)
    # return sigs[:9000]
    times = np.arange(len(sigs))/sameple_rate
    zero_crossings = librosa.zero_crossings(sigs, pad=False)
    print(sum(zero_crossings))
    freqs = nf.fftfreq(sigs.size, 1/sameple_rate)       #报错切成sigs.size-1
    complex_arry = nf.fft(sigs)
    pows = np.abs(complex_arry)
    pows = pows[:10000]

    # return pows
    # print(len(pows))
    fun_freq = freqs[pows.argmax()] #获取频率域中能量最高的
    noised_idx_high = np.where(abs(freqs) >= 2000)[0] #获取所有噪声的下标
    ca = complex_arry[:]
    ca[noised_idx_high] = 1 #高通滤波      之后取对数为0
    noised_idx_low = np.where(abs(freqs) <= 0)[0]
    ca[noised_idx_low] = 1
    # filter_pows = np.abs(complex_arry)
    filter_pows = np.abs(ca)
    db_to = np.log10(filter_pows)
    # print("db_to:",db_to)
    nor_max1 = filter_pows[np.argmax(filter_pows)]
    nor_max = db_to[np.argmax(db_to)]
    # if nor_max==0:
    #     return 0
    # normalization = db_tor_max
    normalization1 = filter_pows/nor_max1
    freq_data=normalization1[0:num]
    return freq_data

#测试函数
@app.route('/')
def hello_world():
    return 'Hello World!'
#测试函数
@app.route('/test1')
def test1():
    if request.method == "GET":
        return "test1"
#接收微信小程序的文件
@app.route('/test2',methods=['POST'])
def test2():
    if request.method == "POST":
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print('上传成功！文件名为：' + filename)
            data = Compose(filename)
            print(data)
        return '文件不存在'

#接收微信小程序上传的文件
@app.route('/upload',methods=['POST'])
def upload():
    if request.method == "POST":
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print('上传成功！文件名为：' + filename)
            data_in = get_peak_data( UPLOAD_FOLDER + '\\'+filename,800)
            data_in = np.array([data_in])
            data = model_single.predict(data_in)
            index = np.argmax(data[0])+40
            print(index)
            note = index_to_note_piano(index-21)
            print(note)
        return note
#接收文件
@app.route('/music',methods=['POST'])
def music():
    if request.method == "POST":
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print('上传成功！文件名为：' + filename)
            note = beat_cut.music_to_note( UPLOAD_FOLDER,filename)
        return note
#和弦检测
@app.route('/chord',methods=['POST'])
def chord():
    if request.method == "POST":
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print('上传成功！文件名为：' + filename)
            data_in = get_peak_data( UPLOAD_FOLDER + '\\'+filename,800)
            data_in = np.array([data_in])
            data = model_hexian.predict(data_in)
            index = np.argmax(data[0])+40
            note1= index_to_note_piano(index-21)
            note2 = index_to_note_piano(index-14)
            print(index)
            print(note1,note2)
        return note1+note2
#文件检测
@app.route('/check',methods=['POST'])
def check():
    if request.method == "POST":
        file = request.files['file']
        id = request.values.get("id")
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print('上传成功！文件名为：' + filename)
            data_in = get_peak_data( UPLOAD_FOLDER + '\\'+filename,10000)
            data_in = np.array([data_in])
            data = model_fenlei.predict(data_in)
            print(data)
            index = np.argmax(data[0])
            print(index)
            return str(index)
#下载文件
@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory("D:/MyCode/MyPython/AiMusicCoach/fluidsynth-x64/bin/",filename,as_attachment=True)

if __name__ == "__main__":
    global filename
    app.run(host='0.0.0.0',port= 5000,debug=True)
