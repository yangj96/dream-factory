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

FLAGS = flags.FLAGS
flags.DEFINE_integer('size', 512, 'The size of the square images to crop.')
flags.DEFINE_integer('min_colors', 2, 'The minimum number of colors per crop.')
flags.DEFINE_string('dataset_dir', 'matting-human-datasets',
                    'The image directory in which to load the dataset.')
flags.DEFINE_string('images_dir', 'crop-images',
                    'The image directory in which to save the crops.')
flags.DEFINE_string('image_format', 'png',
                    'The format under which to save images.')

def main(_):
    if not isdir(FLAGS.images_dir):
        makedirs(FLAGS.images_dir)

    print('Loading images from "%s"' % FLAGS.dataset_dir)
    image_filenames = glob.glob(os.path.join(FLAGS.dataset_dir, 'clip_img', '*', '*', '*.jpg'))
    for img in image_filenames:
        print('Processing: ', img)
        with open(img, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        hash_object = hashlib.sha256(encoded_string)
        hex_dig = hash_object.hexdigest()
        payload = {'data': str(encoded_string, 'utf-8'), 'hash': hex_dig, "trial":"yes"}
        url = 'http://trial.api.infran.grit.id/api/infran/whoisit'
        r = requests.post(url, json=payload)
        response_dict = r.json()
        if response_dict['err_code'] != '0':
            continue
        res = response_dict['data'][0]['pip_loc']
        # crop image according to face location
        image = Image.open(img).convert('RGB')
        # Create the cropped image.
        minn = min(image.height, image.width)
        res_height = res[2] - res[0]
        res_width = res[1] - res[3]
        face_center_x = res_width // 2 + res[3]
        face_center_y = res_height // 2 + res[0]
        crop_half_x = min(res_width * 0.8, min(face_center_x, image.width - face_center_x))
        crop_half_y = min(res_height * 0.8, min(face_center_y, image.height - face_center_y))
        crop_half_v = int(min(crop_half_x, crop_half_y))
        crop = image.crop((face_center_x - crop_half_v, face_center_y - crop_half_v, face_center_x + crop_half_v, face_center_y + crop_half_v)) 
        # Discard predominantly empty crops.
        colors = crop.getcolors()
        if colors and len(colors) < FLAGS.min_colors:
            logging.warning('Skipping empty crop')
            continue
        # resize crop 
        crop = crop.resize((FLAGS.size, FLAGS.size))
        # Save the image
        name = '%s/%s.%s' % (FLAGS.images_dir, hex_dig, FLAGS.image_format)
        crop.save(name, FLAGS.image_format)
        logging.info('Saved %s' % name)
    

if __name__ == '__main__':
    app.run(main)
