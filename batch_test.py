import tensorflow as tf
import keras as k
from keras import layers

# from keras_preprocessing.image import ImageDataGenerator
from keras import preprocessing

from keras.models import clone_model
from keras.applications import ResNet50

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix

import base64
import os

from PIL import Image
import re

from glob import glob

from imglib import processImg

def run_batch():
    # read test data glob and ground truth csv
    test_csv_path = "test_ground_truth/ISIC2018_Task3_Test_GroundTruth/ISIC2018_Task3_Test_GroundTruth.csv"
    df_test = pd.read_csv(test_csv_path)

    df_test['img_name'] = df_test['image'] + ".jpg"

    df_test['bits_num'] = df_test['MEL'] * 1 + df_test['NV'] * 2 + df_test['BCC'] *4 + df_test['AKIEC']*8 +  \
        df_test['BKL']*16 + df_test['DF']*32 + + df_test['VASC']*64

    label_dict = { 1.0 :"mel", 2.0:"nv", 4.0:"bcc", 8.0:"akiec", 16.0:"bkl", 32.0:"df", 64.0:"vasc" }
    def to_dx(bits_num):
        return label_dict.get(bits_num)

    df_test["dx"] = df_test["bits_num"].apply(to_dx)

    #df_val_meta.sample(5)
    print(df_test.head())

    print()
    test_images_path = "test/ISIC2018_Task3_Test_Input/"
    all_imgs = os.listdir(test_images_path)
    print(f"total imgs = {len(all_imgs)}")
    total_correct = 0
    for img_path in all_imgs:
        # print(f"img_path = {img_path}")
        img_base_name = os.path.basename(img_path)
        if not img_base_name.endswith(".jpg"):
            continue
        df_img = df_test[df_test['img_name'] == img_base_name]
        expected_dx = df_img["dx"]
        # print(f"df_img = {df_img}")
        # print(f"expected_dx = {expected_dx}")
        # print(f"expected_dx = {expected_dx.item()}")
        # print(f"expected_dx_type = {type(expected_dx.item())}")
        actual_dx, pct = processImg(os.path.join(test_images_path, img_base_name))
        if actual_dx == expected_dx.item():
            total_correct += 1
            print(".", end="")
        else:
            print("x", end="")

    
    print()
    correct_percentage = 100.0 * total_correct / len(all_imgs)
    print(f"correct percentage = {correct_percentage}%")


if __name__ == "__main__":
    run_batch()