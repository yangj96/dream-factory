# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial
# 4.0 International License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

"""Global configuration."""

#----------------------------------------------------------------------------
# Paths.

result_dir = 'results'
data_dir = 'datasets'
cache_dir = 'cache'
run_dir_ignore = ['results', 'datasets', 'cache']

analysis_data_path = './cache/latent_training_data.pkl'
model_url = './cache/karras2019stylegan-ffhq-1024x1024.pkl'
pretrained_model_path = 'cache/karras2019stylegan-ffhq-1024x1024.pkl'

dlatent_path = './data'

color_map = {'brown': 0, 'gray': 1, 'blond': 2, 'black': 3, 'red': 4}

emotion_map = {'anger': 0, 'contempt': 1, 'disgust': 2, 'fear': 3, 'happiness': 4, 'neutral': 5, 'sadness': 6, 'surprise': 7}


# experimental - replace Dense layers with TreeConnect
use_treeconnect = False
treeconnect_threshold = 1024


#----------------------------------------------------------------------------
