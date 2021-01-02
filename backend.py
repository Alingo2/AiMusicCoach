from flask import Flask,request
import json
import os
UPLOAD_FOLDER = 'D:\MyCode\MyPython\AiMusicCoach\Backend'
app = Flask(__name__, static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024 #上传文件限制为最大 64 MB 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/test1')
def test1():
    if request.method == "GET":
        return "test1"
        
@app.route('/test2')
def test2():
    if request.method == "GET":
        data = request.values.get("a")
        print(data)
        return "succsess"

@app.route('/upload',methods=['POST'])
def upload():
    if request.method == "POST":
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return '上传成功！文件名为：' + filename  #jsonify({'status':'OK','filename':'filename'})
        return '文件不存在'


if __name__ == "__main__":
    app.run(host='0.0.0.0',port= 5000,debug=True)
