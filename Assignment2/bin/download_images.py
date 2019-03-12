import urllib.request
import os

image_list_path = r'F:\Courses\COMP_SCI 5542 - Big Data Analytics and Apps\Source Code\CS5542\Assignment2\data\SBU\SBU_captioned_photo_dataset_urls.txt'
output_path = r'F:\Courses\COMP_SCI 5542 - Big Data Analytics and Apps\Source Code\CS5542\Assignment2\output.txt'
images_path = r'F:\Courses\COMP_SCI 5542 - Big Data Analytics and Apps\Source Code\CS5542\Assignment2\imgs\\'


def download_sbu_images():
    with open(image_list_path) as f:
        images = f.readlines()

    with open(output_path) as f:
        lists = f.readlines()

    for list_species in lists:
        columns = list_species.split()
        species = columns[0]

        folder_path = images_path + species
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        count = 0
        while count < int(columns[1]):
            url = images[int(columns[count + 2])]
            urllib.request.urlretrieve(url, folder_path + "\\" + species + str(count) + ".jpg")
            count += 1


if __name__ == '__main__':
    download_sbu_images()
