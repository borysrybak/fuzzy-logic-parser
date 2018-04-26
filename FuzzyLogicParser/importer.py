# !/usr/bin/python3
# coding: utf-8

# Copyright 2015-2018
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import post

from PIL import Image
from send2trash import send2trash

THIS_FOLDER = os.getcwd()
INPUT_FOLDER = os.path.join(THIS_FOLDER, "img")
RESIZEDIMG_FOLDER = os.path.join(INPUT_FOLDER, "resizedimg")

def prepare_folders():
    """
    :return: void
        Creates necessary folders
    """

    for folder in [INPUT_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)


def find_images(folder):
    """
    :param folder: str
        Path to folder to search
    :return: generator of str
        List of images in folder
    """

    for file in os.listdir(folder):
        full_path = os.path.join(folder, file)
        if os.path.isfile(full_path):
            try:
                _ = Image.open(full_path)  # if constructor succeeds
                yield file
            except:
                pass

def ocr_images():
    images = list(find_images(INPUT_FOLDER))

    for image in images:
        input_path = os.path.join(INPUT_FOLDER, image)
        result = post.post_ocr(input_path)
        print(result)


def main():
    prepare_folders()
    ocr_images()

if __name__ == '__main__':
    main()
