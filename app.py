from flask import Flask, request
from werkzeug.utils import secure_filename
from distance import calculate_distance
import os, os.path, json

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'upload'

@app.route("/", methods=["POST"])
def index():
    file = request.files['image']
    if not os.path.exists('upload'):
        os.mkdir('upload')
    file.save(os.path.join(app.config['UPLOAD_PATH'],  secure_filename(file.filename)))
    file_path = app.config['UPLOAD_PATH'] + '/' + file.filename
    distances = calculate_distance()
    os.remove(file_path)
    if len(distances) < 1 :
        return json.dumps({"distance": 0})
    distance_in_cm = json.dumps({"distance": distances[0]})
    return distance_in_cm