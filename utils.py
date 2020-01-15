from matplotlib import pyplot as plt
import numpy as np

class Shower():
    def __init__(self, col=2):
        self.col = col
        self.objs = []

    def add(self, obj):
        if not isinstance(obj, dict):
            obj = {'image': obj}
        self.objs.append(obj)

    def show(self, save_name=None):
        plt.subplots_adjust(wspace=0)
        n, row, col = len(self.objs), (len(self.objs) + self.col - 1) // self.col, self.col
        for i, obj in enumerate(self.objs):
            image = obj['image']
            plt.subplot(row, col, i + 1)
            plt.axis('off')
            plt.imshow(image)
            if 'title' in obj:
                plt.title(obj['title'])
        if save_name is not None:
            plt.savefig('./examples/{}.png'.format(save_name))
        plt.show()

def softmax(arr):
    arr_exp = np.exp(arr)
    arr_exp_sum = np.sum(arr_exp, axis=1, keepdims=True)
    return arr_exp / arr_exp_sum
