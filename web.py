import time
import os
from flask import Flask, request, render_template, flash, send_from_directory
from src import cnnModel
from src import util
from src import dataPreprocess


# Uploaded image folder
UPLOAD_FOLDER = 'images/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# Predictive model path
modelPath = './models/'
models = []
for i in range(3):
    print('loading model '+str(i))
    models.append(cnnModel.loadModelFromFile(modelPath + 'dataType' + str(i) + '-epoch45-size256.h5'))


# Diagnose a tongue picture
def stDiagnose(imgPath):
    print("predicting: " + imgPath)
    x = util.getImageMatrix(imgPath)
    x = dataPreprocess.preprocessImgMatrix(x)
    x = x.reshape([1] + list(x.shape))
    res = []
    for i in range(3):
        res.append(models[i].predict_on_batch(x).tolist()[0])
        # res.append(models[i].predict_on_batch(x))
    print(res)
    # res = [[0.0, 1.0, 0.0], [0, 0.1, 0.9999, 0.0], [0.0, 1.0]]
    return res


# Define a function to check if an extension is valid
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# Create a Flask server
app = Flask(__name__, static_folder='/static', static_url_path='')
# Set up upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Set up static folder
app._static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


@app.route('/', methods=['GET', 'POST'])
def home():
    res = [[0.0, 1.0, 0.0], [0, 0.1, 0.9999, 0.0], [0.0, 1.0]]
    labelDict = {0: {0: '舌色偏红', 1: '舌色正常', 2: '舌色偏紫'},
                 1: {0: '无舌苔', 1: '舌苔正常', 2: '舌苔偏白', 3: '舌苔偏黄'},
                 2: {0: '无齿痕', 1: '有齿痕'}}
    picName = 'st.jpg'
    if request.method == 'GET':
        return render_template('base.html', results=res, labelDict=labelDict, picName=picName)
    elif request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template('base.html', results=res, labelDict=labelDict)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return render_template('base.html', results=res, labelDict=labelDict)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            filename = str(time.time()) + '.jpg'
            # file_path = 'images/' + filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # image_path = '/home/bach/tongue-diag/web/images/' + filename
            file.save(image_path)
            res = stDiagnose(image_path)
            # return redirect(url_for('predict'))
            return render_template('base.html', results=res, labelDict=labelDict, picName=filename)


@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)


@app.route('/images/<path:filename>')
def serve_images(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'images'), filename)


#if __name__ == '__main__':
#    app.run(host='0.0.0.0')
