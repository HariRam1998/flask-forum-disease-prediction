# Import necessary libraries
from flask import Flask, render_template, request

import numpy as np
import os

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model

# load model
def pred_cot_dieas(plant):
    model = load_model("v6_pred_cott_dis.h5")
    abc = {'Apple___Apple_scab': 0, 'Apple___Black_rot': 1, 'Apple___Cedar_apple_rust': 2, 'Apple___healthy': 3,
           'Blueberry___healthy': 4, 'Cherry_(including_sour)___Powdery_mildew': 5,
           'Cherry_(including_sour)___healthy': 6, 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 7,
           'Corn_(maize)___Common_rust_': 8, 'Corn_(maize)___Northern_Leaf_Blight': 9, 'Corn_(maize)___healthy': 10,
           'Grape___Black_rot': 11, 'Grape___Esca_(Black_Measles)': 12,
           'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': 13, 'Grape___healthy': 14,
           'Orange___Haunglongbing_(Citrus_greening)': 15, 'Peach___Bacterial_spot': 16, 'Peach___healthy': 17,
           'Pepper,_bell___Bacterial_spot': 18, 'Pepper,_bell___healthy': 19, 'Potato___Early_blight': 20,
           'Potato___Late_blight': 21, 'Potato___healthy': 22, 'Raspberry___healthy': 23, 'Soybean___healthy': 24,
           'Squash___Powdery_mildew': 25, 'Strawberry___Leaf_scorch': 26, 'Strawberry___healthy': 27,
           'Tomato___Bacterial_spot': 28, 'Tomato___Early_blight': 29, 'Tomato___Late_blight': 30,
           'Tomato___Leaf_Mold': 31, 'Tomato___Septoria_leaf_spot': 32,
           'Tomato___Spider_mites Two-spotted_spider_mite': 33, 'Tomato___Target_Spot': 34,
           'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 35, 'Tomato___Tomato_mosaic_virus': 36, 'Tomato___healthy': 37}

    test_image = load_img(plant, target_size=(150, 150))  # load image
    print("@@ Got Image for prediction")

    test_image = img_to_array(test_image) / 255  # convert image to np array and normalize
    test_image = np.expand_dims(test_image, axis=0)  # change dimention 3D to 4D
    print(model)
    result = model.predict(test_image).round(3)  # predict diseased palnt or not
    # y_classes = result[0:]
    # print(y_classes)
    print('@@ Raw result = ', result)
    pred = np.argmax(result)  # get the index of max value
    # itemindex=np.where(pred==np.max(pred))
   #  print(label_binarizer.classes_[itemindex[1][0]])
    for key in abc:
        if pred == abc[key]:
            hj = key
            return hj
