import numpy as np
import pandas as pd
import math
from keras import models, layers

'''
@:param data: the original array of floating-point data, which should be normalized 
@:param lookback: How many 
timesteps back in the input data we should go 
@:param delay: How many timesteps in the future the target should be 
@:param min_index and max_index: indices in the data array that delimit which timesteps to draw from (useful for 
keeping parts for validation and testing if necessary) 
@:param shuffle: whether to shuffle the samples or keep them 
in chronological order 
@:param batch_size: the number of samples per batch 
@:param step: the period, in timesteps, 
at which we sample the data '''


def generator(data, lookback, delay, min_index, max_index, shuffle=False, batch_size=128, step=6):
    if max_index is None:
        max_index = len(data) - delay - 1
    i = min_index + lookback
    while 1:
        if shuffle:
            rows = np.random.randint(min_index + lookback, max_index, size=batch_size)
        else:
            if i + batch_size >= max_index:
                i = min_index + lookback
            rows = np.arange(i, min(i + batch_size, max_index))
            i += len(rows)
        samples = np.zeros((len(rows), lookback//step, data.shape[-1]))
        targets = np.zeros((len(rows),))
        for j, row in enumerate(rows):
            indices = range(rows[j] - lookback, rows[j], step)
            samples[j] = data[indices]
            targets[j] = data[rows[j] + delay][1]
        yield samples, targets


def normalize(data):
    mean = data.mean(axis=0)
    data -= mean
    std = data.std(axis=0)
    data /= std


def split_data(data, labels):
    train_set = data.sample(frac=0.8, random_state=0)
    test_set = data.drop(train_set.index)
    train_labels = train_set.pop(labels)
    test_labels = test_set.pop(labels)
    return [train_set, train_labels, test_set, test_labels]

#
# def normalize(data):
#     mean = data[:math.ceil(len(data)*0.66)].mean(axis=0)
#     data -= mean
#     std = data[:math.ceil(len(data)*0.66)].std(axis=0)
#     data /= std
#     return data

