from nltk.tokenize import sent_tokenize, word_tokenize, regexp_tokenize
from shutil import copy2, move
import os
import module.utils as utils

FLICKR8K_CAPTIONS_FILE = "F:\Courses\COMP_SCI 5542 - Big Data Analytics and Apps\Dataset\Flickr8k\Flickr8k_text\Flickr8k.token.txt"
FLICKR8K_IMAGES_FILE = "F:\Courses\COMP_SCI 5542 - Big Data Analytics and Apps\Dataset\Flickr8k\Flickr8k_Dataset\Flicker8k_Dataset\\"
FLICKR30K_CAPTIONS_FILE = "F:\Courses\COMP_SCI 5542 - Big Data Analytics and Apps\Dataset\\flickr30k_images\\results_20130124.token"
FLICKR30K_IMAGES_FILE = "F:\Courses\COMP_SCI 5542 - Big Data Analytics and Apps\Dataset\\flickr30k_images\\flickr30k_images\\"
OUTPUT_CAPTIONS = utils.project_dir_name() + "assets/captions.txt"
ANIMALS_DATASET_DIR = "dataset\\train\\"
ANIMALS_TEST_DIR = "dataset\\test\\"

# categories = ["dog", "cat", "horse", "bird"]
#
# animals_count = [0, 0, 0, 0]

categories = ["dog", "cat", "bird"]

animals_count = [0, 0, 0]

if not os.path.exists('dataset/'):
    os.mkdir('dataset/')

# if not os.path.exists(ANIMALS_DATASET_DIR):
#     os.mkdir(ANIMALS_DATASET_DIR)

if not os.path.exists(ANIMALS_TEST_DIR):
    os.mkdir(ANIMALS_TEST_DIR)

output_captions = open(OUTPUT_CAPTIONS, "w")

with open(FLICKR30K_CAPTIONS_FILE, encoding="utf8") as f:
    captions = f.read().splitlines()

i = 0
while i < len(captions)-5:
    for j in range(5):
        words = regexp_tokenize(captions[i+j], pattern='\w+\.\w+|\w+|#\d+')
        for word in words:
            if word in categories:
                for k in range(5):
                    output_captions.write(word + "." + str(animals_count[categories.index(word)]) + "." + captions[i+k].split(".", 1)[1])
                    output_captions.write("\n")

                src = FLICKR30K_IMAGES_FILE + words[0]
                des = ANIMALS_TEST_DIR + word + "." + str(animals_count[categories.index(word)]) + ".jpg"
                copy2(src, des)

                animals_count[categories.index(word)] += 1
                break
        break
    i += 5

# for i in range(min(animals_count)):
#     for animal in categories:
#         src = ANIMALS_DATASET_DIR + animal + "." + str(i) + ".jpg"
#         des = ANIMALS_TEST_DIR + animal + "." + str(i) + ".jpg"
#         move(src, des)

with open(utils.project_dir_name() + "image_statistic.txt", "w") as istat:
    for index in range(len(categories)):
        istat.write(categories[index] + " " + str(animals_count[index]) + "\n")
