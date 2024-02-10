from flask import Flask, render_template, request
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

# from imglib import processImg   # for keras and tensorflow

from imglib_fastai import processImg  # for fastai

# Initializing flask application
app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def main():
    # return """
    #     Application is working
    # """
    return render_template("index.html")

# About page with render template
@app.route("/about")
def postsPage():
    return render_template("about.html")

# Process images
@app.route("/process", methods=["POST"])
def processRequest():
    try:
        data = request.form["img_content"]
        # print("img_content")
        # print(data[:50])
        pattern = re.compile(r'^data:image/(?P<mime>[a-z]{3,4});base64,(?P<stuff>.+)')
        matchObject = pattern.search(data)
        if matchObject is not None:
            dataDict = matchObject.groupdict()
            if dataDict is not None and 'mime' in dataDict.keys() and 'stuff' in dataDict.keys():
                imgType = dataDict['mime']
                imgBase64 = dataDict['stuff']
                if imgType in ['jpeg', 'png'] and imgBase64 is not None:
                    imgBytes = imgBase64.encode("ascii")
                    decodedBytes = base64.decodebytes(imgBytes)
                    new_filepath = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
                    #new_filepath = f"{new_filepath}.{imgType}"
                    with open(new_filepath, "wb") as binary_file:
                        # Write bytes to file
                        binary_file.write(decodedBytes)
                    
                    if imgType == 'png':
                        print("convert png to jpg")
                        im = Image.open(new_filepath)
                        rgb_im = im.convert('RGB')
                        jpg_path = f"{new_filepath}.jpg"
                        rgb_im.save(jpg_path, quality=100)
                        os.remove(new_filepath)
                        new_filepath = jpg_path

                    flower_name, confidence_percent = processImg(new_filepath)
                    confidence_percent_str = "{:.2f}".format(confidence_percent)
                    os.remove(new_filepath)

                    print("response normal...")

                    #return flower_name
                    return render_template("response.html", flower_name=flower_name, confidence_percent_str=confidence_percent_str, img_base64_str=imgBase64)
            
            print("resopnse file error.")
            return render_template("error.html", error_message="File Processing Error", details="")
    except Exception as ex:
        print("ERROR: ", ex)
        return render_template("error.html", error_message="Server Error", details="{ex}")

                


    return render_template("index.html")

def processRequest_old():
    data = request.files["fileToUpload"]
    new_filepath = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
    # data.save("img.jpg")
    data.save(new_filepath)

    with open(new_filepath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    #flower_name, confidence_percent = processImg("img.jpg")
    flower_name, confidence_percent = processImg(new_filepath)

    confidence_percent_str = "{:.2f}".format(confidence_percent)

    os.remove(new_filepath)

    #return flower_name
    return render_template("response.html", flower_name=flower_name, confidence_percent_str=confidence_percent_str, img_base64_str=encoded_string)



