# from keras.preprocessing.image import img_to_array
from keras.utils import img_to_array
from keras.models import load_model
import cv2
import numpy as np

from flask_cors import CORS, cross_origin

import tensorflow as tf

from datetime import datetime

import base64
import os

from PIL import Image
import re

#names = ["daisy", "dandelon", "roses", "sunflowers", "tulips"]
class_names = ["mel", "nv", "bcc", "akiec", "bkl", "df", "vasc"]



# Process image and predict label
def processImg(img_path):
    img_height = 256
    img_width = 256
    img = tf.keras.utils.load_img(img_path, target_size=(img_height, img_width))

    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    my_dir = os.path.dirname(__file__)
    m_name = os.path.join(my_dir, 'model2.tflite')
    # TF_MODEL_FILE_PATH = 'model.tflite' # The default path to the saved TensorFlow Lite model
    TF_MODEL_FILE_PATH = m_name
    interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)
    sig_dict = interpreter.get_signature_list()
    #print(f"sig_dict = {sig_dict}")
    sig = list(sig_dict)[0]
    #print(f'sig = {sig}')
    classify_lite = interpreter.get_signature_runner('serving_default')
    #print(classify_lite)
    
    # predictions_lite = classify_lite(sequential_1_input=img_array)['outputs']

    predictions_lite = classify_lite(input_2=img_array)['dense_1']
    score_lite = tf.nn.softmax(predictions_lite)
    label_name = class_names[np.argmax(score_lite)]
    confidence_percent = 100 * np.max(score_lite)
    print("This image {} most likely belongs to {} with a {:.2f} percent confidence.".format(img_path, label_name, confidence_percent))

    return label_name, confidence_percent