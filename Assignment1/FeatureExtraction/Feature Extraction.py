import urllib.request
import cv2
import matplotlib.pyplot as plt
import os
import numpy as np


image_path = r'F:\Courses\COMP_SCI 5542 - Big Data Analytics and Apps\Source Code\CS5542\Assignment1\NLP\data\SBU\SBU_captioned_photo_dataset_urls.txt'
caption_path = r'F:\Courses\COMP_SCI 5542 - Big Data Analytics and Apps\Source Code\CS5542\Assignment1\NLP\data\SBU\SBU_captioned_photo_dataset_captions.txt'
theme_path = r'F:\Courses\COMP_SCI 5542 - Big Data Analytics and Apps\Source Code\CS5542\Assignment1\NLP\output.txt'

theme_test = 'water'


def image_detect_and_compute(detector, img_name):
    """Detect and compute interest points and their descriptors."""
    img = cv2.imread(os.path.join(image_path, img_name))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kp, des = detector.detectAndCompute(img, None)
    return img, kp, des

def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


with open(image_path) as f:
    images = f.readlines()

with open(caption_path) as f:
    captions = f.readlines()

with open(theme_path) as f:
    themes = f.readlines()

for theme in themes:
    columns = theme.split()
    if columns[0] == theme_test:
        url_test = columns[3]
        title_test = columns[3]


img_sample = url_to_image(images[int(url_test)])

sift = cv2.xfeatures2d.SIFT_create()
kp, des = sift.detectAndCompute(img_sample, None)
img_kp = cv2.drawKeypoints(img_sample, kp, img_sample)
plt.figure(figsize=(15,  15))
plt.title(captions[int(title_test)])
plt.imshow(img_kp)
plt.show()

