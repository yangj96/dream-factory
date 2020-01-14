import tensorflow as tf
import numpy as np
import dnnlib.tflib as tflib
from functools import partial


def create_stub(name, batch_size):
    return tf.constant(0, dtype='float32', shape=(batch_size, 0))


def create_variable_for_generator(name, batch_size):
    return tf.get_variable('learnable_dlatents',
                           shape=(batch_size, 18, 512),
                           dtype='float32',
                           initializer=tf.initializers.random_normal())


class Generator:
    def __init__(self, model, batch_size, randomize_noise=False):
        self.batch_size = batch_size

        self.initial_dlatents = np.zeros((self.batch_size, 18, 512))
        model.components.synthesis.run(self.initial_dlatents,
                                       randomize_noise=randomize_noise, minibatch_size=self.batch_size,
                                       custom_inputs=[partial(create_variable_for_generator, batch_size=batch_size),
                                                      partial(create_stub, batch_size=batch_size)],
                                       structure='fixed')

        self.sess = tf.get_default_session()
        self.graph = tf.get_default_graph()

        self.dlatent_variable = next(v for v in tf.global_variables() if 'learnable_dlatents' in v.name)
        self.set_dlatents(self.initial_dlatents)

        self.generator_output = self.graph.get_tensor_by_name('G_synthesis_1/_Run/concat:0')
        self.generated_image = tflib.convert_images_to_uint8(self.generator_output, nchw_to_nhwc=True, uint8_cast=False)
        self.generated_image_uint8 = tf.saturate_cast(self.generated_image, tf.uint8)

    def reset_dlatents(self):
        self.set_dlatents(self.initial_dlatents)

    def set_dlatents(self, dlatents):
        assert (dlatents.shape == (self.batch_size, 18, 512))
        self.sess.run(tf.assign(self.dlatent_variable, dlatents))

    def get_dlatents(self):
        return self.sess.run(self.dlatent_variable)

    def generate_images(self, dlatents=None):
        if dlatents:
            self.set_dlatents(dlatents)
        return self.sess.run(self.generated_image_uint8)


if __name__ == '__main__':
    import config
    import pickle
    import cv2
    tflib.init_tf()
    with open(config.pretrained_model_path, 'rb') as f:
        generator_network, discriminator_network, Gs_network = pickle.load(f)
    print(tf.global_variables())

    generator = Generator(Gs_network, batch_size=1, randomize_noise=False)
    
    rnd = np.random.RandomState(5)
    latent_vector = rnd.randn(1, 18, 512)
    print(latent_vector.max(), latent_vector.min(), latent_vector.mean())
    generator.set_dlatents(latent_vector) 
    img = generator.generate_images()[0]
    print(img.shape)
    cv2.imwrite('./results/random.png', img)