"""
This script trains a Convolutional Neural networks that learns a mapping between potential couple profile pics and
decisions taken by the user (swipe right/left). Once trained, this network will be able to mimic the decision process
carried out by the individual user, effectively swiping according to his/her preferences.
"""

from scipy.misc import imread, imresize
import os
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import Adam
import numpy as np
import pandas as pd


class Swipe:
    def __init__(self, filename, data_location):

        self.pic = imread(os.path.join(data_location, filename), mode='RGB')

        info = os.path.splitext(filename)[0].split('_')

        self.score = info[1]
        self.name = info[2]
        self.age = info[3]
        self.bio = info[4]
        self.city = info[5]


def square_pic(picsz, pic):

    if pic.shape[0] != picsz:
        extra = abs(picsz - pic.shape[0])
        pic = pic[int(extra/2):-int(extra/2), :, :]
    if pic.shape[1] != picsz:
        extra =abs(picsz - pic.shape[1])
        pic = pic[:, int(extra / 2):-int(extra / 2), :]
    return pic


def create_model():
    model = Sequential()
    model.add(Conv2D(64, (5, 5), activation='relu', input_shape=(pic_size, pic_size, 3)))
    model.add(Conv2D(64, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.1))

    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.1))

    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='linear'))

    return model

if __name__ == "__main__":

    data_location = 'train_data'
    pic_size = 128
    image_filenames = [x for x in os.listdir(data_location)]
    swipes = []
    # fill array of swipes
    for file in image_filenames:
        swipes.append(Swipe(file, data_location))

    # create training data
    y_train = np.array([x.score for x in swipes])
    x_train = np.stack([imresize(square_pic(pic_size, x.pic), (pic_size, pic_size))/255 for x in swipes], axis=0)

    # print scores distribution
    print(dict(pd.Series(y_train).value_counts()))

    # create model
    model = create_model()

    model.compile(loss='mean_squared_error', optimizer=Adam())

    model.fit(x_train, y_train, batch_size=32, epochs=3)

    model.save('model/TinderBot.h5')