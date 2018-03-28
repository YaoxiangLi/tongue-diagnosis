import time
import os
from flask import Flask, request, render_template, flash, send_from_directory, redirect, url_for
from src import cnnModel, util, dataPreprocess


# Uploaded image folder
UPLOAD_FOLDER = 'images/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


# Predictive model path
modelPath = './models/'
models = []
for n in range(3):
    print('loading model '+str(n))
    models.append(cnnModel.loadModelFromFile(modelPath + 'dataType' + str(n) + '-epoch45-size256.h5'))


# Diagnose a tongue picture
def st_diagnose(img_path):
    print("predicting: " + img_path)
    x = util.getImageMatrix(img_path)
    x = dataPreprocess.preprocessImgMatrix(x)
    x = x.reshape([1] + list(x.shape))
    ret = []
    for i in range(3):
        ret.append(models[i].predict_on_batch(x).tolist()[0])
        # res.append(models[i].predict_on_batch(x))
    print(ret)
    # ret = [[0.0, 1.0, 0.0], [0, 0.1, 0.9999, 0.0], [0.0, 1.0]]
    return ret


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

res = [[0.0, 1.0, 0.0], [0, 0.1, 0.9999, 0.0], [0.0, 1.0]]
labelDict = {0: {0: '舌色偏红', 1: '舌色正常', 2: '舌色偏紫'},
             1: {0: '无舌苔', 1: '舌苔正常', 2: '舌苔偏白', 3: '舌苔偏黄'},
             2: {0: '无齿痕', 1: '有齿痕'}}
picName = 'st.jpg'


@app.route('/', methods=['GET', 'POST'])
def home():
    global res, labelDict, picName

    if request.method == 'GET':
        return render_template('base.html',
                               results=res,
                               labelDict=labelDict,
                               picName=picName)

    elif request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('home'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('home'))
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            picName = str(time.time()) + '.jpg'
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], picName)
            file.save(image_path)
            res = st_diagnose(image_path)
            return redirect(url_for('home'))


@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)


@app.route('/images/<path:filename>')
def serve_images(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'images'), filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
