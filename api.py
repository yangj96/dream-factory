import config
import dnnlib
import dnnlib.tflib as tflib
from encoder.generator_model import Generator


# config
batch_size = 1
dlatent_path = './data'

tasks = [
    'fuse',
    'gender',
    'age',
    'maskup',
    'hair_color',
    'smile',
    'emotion',
    'glasses',
    'head_yaw',
    'facial_hair',
    'exposure'
]

def run(image_id1, task_type, weight, image_id2=None):
    assert task_type in task