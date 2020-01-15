import os
from os.path import join
import pickle
import json
import numpy as np
import argparse

from keras.models import Sequential, Model
from keras.layers import Dense
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping

import warnings
warnings.filterwarnings("ignore")

import config
from config import color_map, emotion_map
import dnnlib
import dnnlib.tflib as tflib
from encoder.generator_model import Generator
from utils import Shower, softmax

#######################################
# config
batch_size = 1
dlatent_path = './data'
#######################################

print('loading stylegan')
tflib.init_tf()
with open(config.model_url, 'rb') as f:
    generator_network, discriminator_network, Gs_network = pickle.load(f)
generator = Generator(Gs_network, batch_size)
print('loaded stylegan')

print('loadind analysis data')
with open(config.analysis_data_path, 'rb') as f:
    _, dlatent_data, labels_data = pickle.load(f)
print('loaded analysis data')

x_data = dlatent_data.reshape((-1, 18 * 512))


def learn_gender():
    y_gender = np.array([x['faceAttributes']['gender'] == 'male' for x in labels_data])
    model = Sequential()
    model.add(Dense(1, activation='sigmoid'))
    model.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=2)

    model.fit(x_data, y_gender, validation_split=0.2, epochs=100, callbacks=[early_stopping])

    gender_direction = model.layers[0].get_weights()[0]
    gender_direction = gender_direction.reshape(18, 512)
    np.save('./data/gender_direction', gender_direction)


def learn_age():
    y_age = np.array([x['faceAttributes']['age'] for x in labels_data])

    model = Sequential()
    model.add(Dense(1, activation='relu'))
    model.compile('adam', 'mse', metrics=['mse'])
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=2)

    model.fit(x_data, y_age, validation_split=0.2, epochs=100, callbacks=[early_stopping])

    age_direction = model.layers[0].get_weights()[0]
    age_direction = age_direction.reshape(18, 512)
    np.save('./data/age_direction', age_direction)


def learn_makeup():
    y_makeup = np.array([(x['faceAttributes']['makeup']['eyeMakeup'] or x['faceAttributes']['makeup']['eyeMakeup']) for x in labels_data])

    model = Sequential()
    model.add(Dense(1, activation='sigmoid'))
    model.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=2)

    model.fit(x_data, y_makeup, validation_split=0.2, epochs=100, callbacks=[early_stopping])

    makeup_direction = model.layers[0].get_weights()[0]
    makeup_direction = makeup_direction.reshape(18, 512)
    np.save('./data/makeup_direction', makeup_direction)


def learn_hair_color():
    y_hair_color_dict = [x['faceAttributes']['hair']['hairColor'] for x in labels_data]
    y_hair_color = []
    x_for_hair = []

    for i, sample in enumerate(y_hair_color_dict):
        tmp_res = [0] * 5
        maxx, maxx_color = 0, 'other'
        for arr_item in sample:
            color = arr_item['color']
            if color == 'other': continue
            if arr_item['confidence'] >= maxx:
                maxx, maxx_color = arr_item['confidence'], color
        if maxx_color != 'other':
            tmp_res[color_map[maxx_color]] = 1
            y_hair_color.append(tmp_res)
            x_for_hair.append(x_data[i])
    y_hair_color = np.array(y_hair_color)
    x_for_hair = np.array(x_for_hair)

    model = Sequential()
    model.add(Dense(5, activation='softmax'))
    model.compile('adam', 'categorical_crossentropy', metrics=['accuracy'])
    early_stopping = EarlyStopping(monitor='val_loss', patience=20, verbose=2)
    model.fit(x_for_hair, y_hair_color, validation_split=0.2, epochs=100, callbacks=[early_stopping])

    hair_direction = model.layers[0].get_weights()[0].reshape(18, 512, 5)
    np.save('./data/hair_direction', hair_direction)


def learn_smile():
    y_smile = np.array([x['faceAttributes']['smile'] for x in labels_data])

    model = Sequential()
    model.add(Dense(1, activation='sigmoid'))
    model.compile('adam', 'mse', metrics=['mse'])
    early_stopping = EarlyStopping(monitor='val_loss', patience=20, verbose=2)
    model.fit(x_data, y_smile, validation_split=0.2, epochs=100, callbacks=[early_stopping])

    smile_direction = model.layers[0].get_weights()[0].reshape(18, 512)
    np.save('./data/smile_direction', smile_direction)


def learn_emotion():
    y_emotion_dict = [x['faceAttributes']['emotion'] for x in labels_data]
    y_emotion = []
    for i, sample in enumerate(y_emotion_dict):
        tmp_res = [0] * 8
        for typ, val in sample.items():
            tmp_res[emotion_map[typ]] = val
        y_emotion.append(tmp_res)
    y_emotion = np.array(y_emotion)

    model = Sequential()
    model.add(Dense(8, activation='softmax'))
    model.compile('adam', 'categorical_crossentropy', metrics=['accuracy'])
    early_stopping = EarlyStopping(monitor='val_loss', patience=20, verbose=2)

    model.fit(x_data, y_emotion, validation_split=0.2, epochs=100, callbacks=[early_stopping])

    emotion_direction = model.layers[0].get_weights()[0]
    emotion_direction = emotion_direction.reshape(18, 512, 8)
    np.save('./data/emotion_direction', emotion_direction)


def learn_glasses():
    y_glasses = np.array([x['faceAttributes']['glasses'] != 'NoGlasses' for x in labels_data])

    model = Sequential()
    model.add(Dense(1, activation='sigmoid'))
    model.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
    early_stopping = EarlyStopping(monitor='val_loss', patience=20, verbose=2)

    model.fit(x_data, y_glasses, validation_split=0.2, epochs=100, callbacks=[early_stopping])

    glasses_direction = model.layers[0].get_weights()[0]
    glasses_direction = glasses_direction.reshape(18, 512)
    np.save('./data/glasses_direction', glasses_direction)


def learn_head_yaw():
    y_head_yaw = np.array([x['faceAttributes']['headPose']['yaw'] for x in labels_data])

    model = Sequential()
    model.add(Dense(1, activation=None))
    model.compile('adam', 'mse', metrics=['mse'])
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=2)
    model.fit(x_data, y_head_yaw, validation_split=0.2, epochs=100, callbacks=[early_stopping])

    head_yaw_direction = model.layers[0].get_weights()[0].reshape(18, 512)
    np.save('./data/head_yaw_direction', head_yaw_direction)


def learn_facial_hair():
    y_facialHair_dict = [x['faceAttributes']['facialHair'] for x in labels_data]
    y_facialHair = np.array([(x['moustache'] + x['beard'] + x['sideburns']) / 3. for x in y_facialHair_dict])

    model = Sequential()
    model.add(Dense(1, activation='sigmoid'))
    model.compile('adam', 'mse', metrics=['mse'])
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=2)
    model.fit(x_data, y_facialHair, validation_split=0.2, epochs=100, callbacks=[early_stopping])

    facial_hair_direction = model.layers[0].get_weights()[0].reshape(18, 512)
    np.save('./data/facial_hair_direction', facial_hair_direction)


def learn_exposure():
    y_exposure = np.array([x['faceAttributes']['exposure']['value'] for x in labels_data])

    model = Sequential()
    model.add(Dense(1, activation='sigmoid'))
    model.compile('adam', 'mse', metrics=['mse'])
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=2)
    model.fit(x_data, y_exposure, validation_split=0.2, epochs=100, callbacks=[early_stopping])
    
    exposure_direction = model.layers[0].get_weights()[0].reshape(18, 512)
    np.save('./data/exposure_direction', exposure_direction)


if __name__ == '__main__':
    print('learning gender');       learn_gender();       print('end learning gender')
    print('learning age');          learn_age();          print('end learning age')
    print('learning makeup');       learn_makeup();       print('end learning makeup')
    print('learning hair color');   learn_hair_color);    print('end learning hair color')
    print('learning smile');        learn_smile();        print('end learning smile')
    print('learning emotion');      learn_emotion();      print('end learning emotion')
    print('learning glasses');      learn_glasses();      print('end learning glasses')
    print('learning head yaw');     learn_head_yaw();     print('end learning head yaw')
    print('learning facial hair');  learn_facial_hair();  print('end learning facial hair')
    print('learning exposure');     learn_exposure();     print('end learning exposure')