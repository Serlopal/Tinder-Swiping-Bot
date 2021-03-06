"""
This script records the user swipes on the Tinder webiste, to create a database
that maps couple images to decisions (swipe right / swipe left) TODO: use more than the main pic as input
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import msvcrt
from pynput import keyboard
import re
import time
from urllib import request



def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def on_press(key):

    # if key pressed are right or left arrows (pressed by the software to swipe, do nothing)
    try:
        # tell website to like or dislike -> like(3, 4, 5)  dislike (0, 1, 2)
        if key.char in ['0', '1', '2']:
            save_profile(key.char)
            k.press(keyboard.Key.left)
            k.release(keyboard.Key.left)
        elif key.char in ['3', '4', '5']:
            save_profile(key.char)
            k.press(keyboard.Key.right)
            k.release(keyboard.Key.right)
        else:
            pass
    except:
        pass

def on_release(key):
    pass


def save_profile(score):

    global swipec

    soup = BeautifulSoup(driver.page_source, features="html5lib")

    active = soup.find("div", {"class": "active"}) # the class that contains the profile pic has an "active" in its name
    active_picurl = re.findall(r'"(.*?)"', active.find(style = re.compile(".jpg"))["style"])[0] # find picture tag
    info = active.contents[5].text
    active_age = info.split(',')[1][:3].strip()
    # make sure bios do not interfere with underscore separation of fields
    active_bio = info.split(',')[1][3:].strip().replace(" ", "-").replace("_", "-") if info.split(',')[1][3:].strip() else "none"
    active_name = info.split(',')[0]

    filename = "{0}_{1}_{2}_{3}_{4}_{5}.jpg".format(time.time(), score, active_name, active_age, active_bio, city)

    request.urlretrieve(active_picurl, "E:/PythonScripts/TinderExp/data2/" + get_valid_filename(filename))
    swipec += 1
    print("saved swipe " + str(swipec))


# global variable storing the number of stored swipes
swipec = 0

if __name__ == "__main__":

    city = "madrid"

    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=C:/Users/Ferraat/AppData/Local/Google/Chrome/User Data")


    driver = webdriver.Chrome(executable_path="E:\PythonScripts\TinderExp\chromedriver.exe", options=options)
    driver.get('http://tinder.com')

    k = keyboard.Controller()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()



