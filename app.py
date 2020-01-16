import sys
import json
import os
import time
import shutil
import numpy as np
from glob import glob
from PIL import Image
from flask import Flask, request, jsonify, abort, Response
from flask_cors import *
import base64
import cv2

import api as API

app = Flask(__name__)
CORS(app, supports_credentials=True)

mdict = {
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif'
}

image_names = [x for x in os.listdir('./images')]
image_ids = [x.split('.')[0] for x in image_names]


def get_id(image_name):
    return image_name.split('.')[0]


@app.route('/imagenames', methods=['GET'])
def get_imagenames():
    return jsonify(image_names=image_names, image_ids=image_ids)


@app.route('/image/gan/<image_name>', methods=['GET'])
def get_gan_image(image_name):
    try:
        image_id = get_id(image_name)
    except:
        abort(404)
    image_path = './data/{}'.format(image_name)
    mime = mdict[image_name.split('.')[-1]]
    if not os.path.exists(image_path) or image_name not in image_names:
        abort(404)
    
    with open(image_path, 'rb') as f:
        image = f.read()
    return Response(image, mimetype=mime)


@app.route('/image/<image_name>', methods=['GET'])
def get_image(image_name):
    try:
        image_id = get_id(image_name)
    except:
        abort(404)
    image_path = './images/{}'.format(image_name)
    mime = mdict[image_name.split('.')[-1]]
    if not os.path.exists(image_path) or image_name not in image_names:
        abort(404)
    
    with open(image_path, 'rb') as f:
        image = f.read()
    return Response(image, mimetype=mime)


@app.route('/run', methods=['GET'])
def generate_image():
    image_id1 = request.args.get('image_id1')
    image_id2 = request.args.get('image_id2')
    weight = request.args.get('weight')
    task_type = request.args.get('task_type')
    choice = request.args.get('choice')
    resolution = request.args.get('resolution')
    print(image_id1, image_id2, weight, task_type, resolution)

    if image_id1 is None or task_type is None:
        abort(404)
    if weight is not None:
        try:
            weight = float(weight)
        except:
            abort(404)
    if resolution is not None:
        try: resolution = int(resolution)
        except: abort(404)

    start = time.time()
    images = API.run(image_id1, task_type, weight, image_id2=image_id2, choice=choice, resolution=resolution)
    print('Cost', time.time() - start)

    for i, image in enumerate(images):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_str = cv2.imencode('.png', image)[1].tostring()
        images[i] = base64.b64encode(img_str).decode('ascii')

    return jsonify(images=images)


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
    app.run(host="0.0.0.0", port=5000, debug=False)
