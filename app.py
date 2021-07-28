from flask import Flask, request
from werkzeug.utils import secure_filename
from distance import calculate_distance
import os, os.path

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'upload'

@app.route("/", methods=["POST"])
def index():
    file = request.files['image']
    print(file.filename)
    if not os.path.exists('upload'):
        os.mkdir('upload')
    file.save(os.path.join(app.config['UPLOAD_PATH'],  secure_filename(file.filename)))
    file_path = app.config['UPLOAD_PATH'] + '/' + file.filename
    distance_in_cm = ' '.join(map(str, calculate_distance()))
    os.remove(file_path)
    return distance_in_cm
