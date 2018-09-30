"""
This script trains a Convolutional Neural networks that learns a mapping between potential couple profile pics and
decisions taken by the user (swipe right/left). Once trained, this network will be able to mimic the decision process
carried out by the individual user, effectively swiping according to his/her preferences.
"""

from scipy.misc import imread, imresize
import os


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

if __name__ == "__main__":

    data_location = 'data2'

    image_filenames = [os.path.join(data_location, x) for x in os.listdir(data_location)]

    swipes = []

    for file in image_filenames:
        swipes.append(Swipe(file))
    print("asd")