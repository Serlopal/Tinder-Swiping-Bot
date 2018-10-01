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


class Swipe:
    def __init__(self, filename):

        self.pic = imread(filename, mode='RGB')

        info = os.path.splitext(filename)[0].split('_')

        self.swipe = 1 if info[1]=='like' else 0
        self.dectime = info[2]
        self.name = info[3]
        self.age = info[4]
        self.bio = info[5]
        self.city = info[6]


def square_pic(picsz, pic):

    if pic.shape[0] != picsz:
        extra = abs(picsz - pic.shape[0])
        pic = pic[int(extra/2):-int(extra/2), :, :]
    if pic.shape[1] != picsz:
        extra =abs(picsz - pic.shape[1])
        pic = pic[:, int(extra / 2):-int(extra / 2), :]
    return pic

if __name__ == "__main__":

    data_location = 'data2'

    pic_size = 128

    image_filenames = [os.path.join(data_location, x) for x in os.listdir(data_location)]

    swipes = []

    for file in image_filenames:
        swipes.append(Swipe(file))


    # create training data
    y_train = np.array([x.swipe for x in swipes])
    x_train = np.stack([imresize(square_pic(pic_size, x.pic), (pic_size, pic_size)) for x in swipes], axis=0)

    # create model

    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(pic_size, pic_size, 3)))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer=Adam())

    model.fit(x_train, y_train, batch_size=32, epochs=10)
