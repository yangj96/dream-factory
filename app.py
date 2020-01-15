import sys
import cv2
import json
import os
import time
import shutil
import numpy as np
from glob import glob
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/test', methods=['POST', 'GET'])
def test():
    return "don't worry, be happy"


@app.route('/ocr', methods=['POST'])
def generate_image():
    img = request.files.get('image')

    res = []
    for item in arr:
        res.append({
            'DetectedText': item[-1],
            'Polygon': [{
                'X': x,
                'Y': y
            } for x, y in item[:-1]]
        })
    res = {'TextDetections': res}
    return jsonify(res)


class JSONEncoder(json.JSONEncoder):
    
    def default(self, o):
        if isinstance(o, np.integer):
            return int(o)
        elif isinstance(o, np.floating):
            return float(o)
        elif isinstance(o, np.ndarray):
            return o.tolist()
        else:
            return super(JSONEncoder, self).default(o)


if __name__ == '__main__':
    app.json_encoder = JSONEncoder
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", port=443, debug=True)