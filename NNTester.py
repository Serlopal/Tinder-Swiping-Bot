from scipy.misc import imread, imresize
import os
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import Adam
import numpy as np
from keras.models import load_model
from NNTrainer import Swipe, square_pic

if __name__ == "__main__":

    data_location = 'test_data'

    pic_size = 256

    image_filenames = [x for x in os.listdir(data_location)]

    swipes = []

    for file in image_filenames:
        swipes.append(Swipe(file, data_location))


    # create training data
    y_test = np.array([x.score for x in swipes])
    x_test = np.stack([imresize(square_pic(pic_size, x.pic), (pic_size, pic_size))/255 for x in swipes], axis=0)


    model = load_model('model/TinderBot.h5')

    preds = model.predict(x_test)
    print(preds)



