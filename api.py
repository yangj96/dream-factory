import pickle
import numpy as np
import os
from os.path import join
import cv2

import config
from config import dlatent_path, emotion_map, hair_color_map
import dnnlib
import dnnlib.tflib as tflib
from encoder.generator_model import Generator


# config
batch_size = 1

tasks = [
    'fuse',
    'gender',
    'age',
    'makeup',
    'hair',
    'smile',
    'emotion',
    'glasses',
    'head_yaw',
    'facial_hair',
    'exposure'
]

dlatent_directions = dict()

###################################################
print('Init')
tflib.init_tf()
with open(config.model_url, 'rb') as f:
    generator_network, discriminator_network, Gs_network = pickle.load(f)
generator = Generator(Gs_network, batch_size)

print('Load dlatent direction vectors')
for task in tasks:
    if task == 'fuse':
        continue
    dlatent_directions[task] = np.load('./data/{}_direction.npy'.format(task))
print('Loaded')    

def load_dlatent(image_id):
    dl_path = join(dlatent_path, image_id + '.npy')
    dlatent = np.load(dl_path)
    dlatent = dlatent.reshape(-1, 18, 512)
    return dlatent

def run_fuse(image_id1, image_id2):
    dlatent1 = load_dlatent(image_id1)
    dlatent2 = load_dlatent(image_id2)
    res = []
    for w in [0.2, 0.35, 0.45, 0.55, 0.7, 0.8]:
        new_dlatent = dlatent1 * (1 - w) + dlatent2 * w
        res.append(generator.generate_images(new_dlatent)[0])
    return res

def run_simple(image_id, weight, task):
    '''
    for some simple-case applications
    '''
    dlatent = load_dlatent(image_id)
    dlatent = dlatent + weight * dlatent_directions[task]
    res = generator.generate_images(dlatent)[0]
    return res

def run_emotion(image_id, weight, choice):
    dlatent = load_dlatent(image_id)
    idx = emotion_map[choice]
    dlatent_direction = dlatent_directions['emotion'][..., idx]
    dlatent = dlatent + weight * dlatent_direction
    res = generator.generate_images(dlatent)[0]
    return res

def run_hair(image_id, weight, choice):
    dlatent = load_dlatent(image_id)
    idx = hair_color_map[choice]
    dlatent_direction = dlatent_directions['hair'][..., idx]
    dlatent = dlatent + weight * dlatent_direction
    res = generator.generate_images(dlatent)[0]
    return res

def run(image_id1, task_type, weight, image_id2=None, choice=None):
    assert task_type in tasks
    assert task_type != 'fuse' or image_id2 is not None
    
    if task_type == 'fuse':
        res = run_fuse(image_id1, image_id2)
    elif task_type == 'emotion':
        assert choice in emotion_map
        res = run_emotion(image_id1, weight, choice)
    elif task_type == 'hair':
        assert choice in hair_color_map
        res = run_hair(image_id1, weight, choice)
    else:
        res = run_simple(image_id1, weight, task_type)
    
    if isinstance(res, list):
        for i, image in enumerate(res):
            res[i] = cv2.resize(image, (128, 128))
    else:
        res = cv2.resize(res, (128, 128))
        res = [res]
    return res
    