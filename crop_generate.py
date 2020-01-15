import os
import sys
import glob
import requests
import hashlib
import base64
import json
import PIL.Image
from absl import app
from absl import flags
from absl import logging
from os import makedirs
from os.path import isdir
from PIL import Image
import cv2
import numpy
import dlib

FLAGS = flags.FLAGS
flags.DEFINE_integer('size', 512, 'The size of the square images to crop.')
flags.DEFINE_integer('min_colors', 2, 'The minimum number of colors per crop.')
flags.DEFINE_string('dataset_dir', 'matting-human-datasets',
                    'The image directory in which to load the dataset.')
flags.DEFINE_string('images_dir', 'crop-images',
                    'The image directory in which to save the crops.')
flags.DEFINE_string('image_format', 'png', 'The format under which to save images.')


def rect_to_bb(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return (x, y, w, h)


def main(_):
    if not isdir(FLAGS.images_dir):
        makedirs(FLAGS.images_dir)

    print('Loading images from "%s"' % FLAGS.dataset_dir)
    image_filenames = glob.glob(os.path.join(FLAGS.dataset_dir, 'clip_img', '*', '*', '*.jpg'))
    # image_filenames = ['1803251855-00000022.jpg', '1803251855-00000066.jpg']
    for img in image_filenames:
        print('Processing: ', img)
        # with open(img, "rb") as image_file:
        #     encoded_string = base64.b64encode(image_file.read())
        # hash_object = hashlib.sha256(encoded_string)
        # hex_dig = hash_object.hexdigest()
        # payload = {'data': str(encoded_string, 'utf-8'), 'hash': hex_dig, "trial":"yes"}
        # url = 'http://trial.api.infran.grit.id/api/infran/whoisit'
        # r = requests.post(url, json=payload)
        # response_dict = r.json()
        # if response_dict['err_code'] != '0':
        #     continue
        # res = response_dict['data'][0]['pip_loc']
        
        # crop image according to face location
        image = Image.open(img).convert('RGB')
        # face_cascade = cv2.CascadeClassifier()
        image_gray = cv2.cvtColor(numpy.asarray(image), cv2.COLOR_BGR2GRAY)
        # image_gray = cv2.equalizeHist(image_gray)
        # res = face_cascade.detectMultiScale(image_gray)
        detector = dlib.get_frontal_face_detector() # cnn_face_detection_model_v1 also can be used
        res  = detector(image_gray, 1)
        
        # Create the cropped image.
        # print(res[0])
        (x, y, res_width, res_height) = rect_to_bb(res[0])
        minn = min(image.height, image.width)
        face_center = (x + res_width//2, y + res_height//2)
        crop_half_x = min(res_width * 0.9, min(face_center[0], image.width - face_center[0]))
        crop_half_y = min(res_height * 0.9, min(face_center[1], image.height - face_center[1]))
        crop_half_v = int(min(crop_half_x, crop_half_y))
        crop = image.crop((face_center[0] - crop_half_v, face_center[1] - crop_half_v, face_center[0] + crop_half_v, face_center[1] + crop_half_v)) 
        # Discard predominantly empty crops.
        colors = crop.getcolors()
        if colors and len(colors) < FLAGS.min_colors:
            logging.warning('Skipping empty crop')
            continue
        # resize crop 
        crop = crop.resize((FLAGS.size, FLAGS.size))
        # Save the image
        name = '%s/%s.%s' % (FLAGS.images_dir, os.path.split(img)[-1].split('.')[0], FLAGS.image_format)
        crop.save(name, FLAGS.image_format)
        logging.info('Saved %s' % name)
    

if __name__ == '__main__':
    app.run(main)
