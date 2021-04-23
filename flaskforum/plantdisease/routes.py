#!/usr/bin/env python
import os
import shutil
from flask import Flask, render_template, request, \
    Response, send_file, redirect, url_for
# from send_email import Email
from flaskforum.plantdisease import disease_solution
from flaskforum.plantdisease.camera import Camera
from flaskforum.plantdisease.send_email import Email
from flask import render_template, current_app, url_for, flash, redirect, request, Blueprint
from flask_login import login_required, login_user, current_user, logout_user
from flaskforum.users.forms import LoginForm, RegisterForm, UpdateAccountForm
from flaskforum.replies.forms import ReplyForm
from flaskforum import db, bcrypt
from flaskforum.models import User, Post, Vote, Reply
import os
import flaskforum.plantdisease.disease_solution
import secrets
from PIL import Image
import test
import numpy as np
import os
#from flaskforum.plantdisease.test import pred_cot_dieas
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model


plantdisease = Blueprint('plantdisease', __name__)
camera = None
mail_server = None
mail_conf = "static/mail_conf.json"
imagefile = "static/download.jpg"
path = 0
model = load_model("C:/Users/Hari Ram/Downloads/flask-forum-master/flaskforum/plantdisease/v6_pred_cott_dis.h5")
print(model)
# load model

def pred_cot_dieas(cottplant):
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

    test_image = load_img(cottplant, target_size=(150, 150))  # load image
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


def sendpic(a):
    path =a

def get_camera():
    global camera
    if not camera:
        camera = Camera()

    return camera

def get_mail_server():
    global mail_server
    if not mail_server:
        mail_server = Email(mail_conf)

    return mail_server

@plantdisease.route('/')
def root():
    return redirect(url_for('index'))


@plantdisease.route('/select/')
def select():
    if current_user.is_authenticated:
        image_file1 = url_for('static', filename='profiles/' + current_user.image_file)
        return render_template('diseasemodule.html',image_file=image_file1)
    else:
        return render_template('diseasemodule.html', image_file=imagefile)


@plantdisease.route('/index/')
def camon():
    if current_user.is_authenticated:
        image_file1 = url_for('static', filename='profiles/' + current_user.image_file)
        return render_template('index.html', image_file=image_file1)
    else:
        return render_template('index.html', image_file=imagefile)


def gen(camera):
    while True:
        frame = camera.get_feed()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@plantdisease.route('/video_feed/')
def video_feed():
    camera = get_camera()
    return Response(gen(camera),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@plantdisease.route('/capture/')
def capture():
    camera = get_camera()
    stamp = camera.capture()
    return redirect(url_for('plantdisease.show_capture', timestamp=stamp))

def stamp_file(timestamp):
    return 'captures/' + timestamp +".jpg"

@plantdisease.route('/capture/image/<timestamp>', methods=['POST', 'GET'])
def show_capture(timestamp):
    global path
    path = stamp_file(timestamp)
    sendpic(path)

    print(path)
    if current_user.is_authenticated:
        image_file1 = url_for('static', filename='profiles/' + current_user.image_file)
        return render_template('capture.html',
            stamp=timestamp, path=path,image_file=image_file1)
    else:
        return render_template('capture.html',
                               stamp=timestamp, path=path, image_file=imagefile)

@plantdisease.route('/cropai', methods=['GET', 'POST'])
def croppredict():

    print("hello", path)
    abc = str(path)
    abc = abc.split('/')
    print(abc)
    file_path1 = url_for('static', filename='captures/' + abc[1])
    file_path = os.path.join(current_app.root_path, 'static/captures',abc[1])
    # file_path = "../static/user uploaded/hari.jpg"
    # b = 'static/'+path
    a = pred_cot_dieas(file_path)
    crop_data = disease_solution.crop(a)
    context = {
        "image1": crop_data[0],
        "image2": crop_data[1],
        "image3": crop_data[2],
        "details": crop_data[3],
        "info1": crop_data[4],
        "info2": crop_data[5],
        "info3": crop_data[6],
        "price1": crop_data[7],
        "price2": crop_data[8],
        "price3": crop_data[9],

    }
    if current_user.is_authenticated:
        image_file1 = url_for('static', filename='profiles/' + current_user.image_file)
        return render_template('cropai.html', image_file=image_file1,user_image = file_path1 , pred_output = a, context=context)
    else:
        return render_template('cropai.html',user_image = file_path1, pred_output = a, context=context)


@plantdisease.route('/predictupload', methods=['GET', 'POST'])
def predictupload():
    file = request.files['image']  # fet input
    filename = file.filename
    print("@@ Input posted = ", filename)
    file_path = os.path.join(current_app.root_path,'static/user uploaded', filename)
    file.save(file_path)
    # picture_path = os.path.join(current_app.root_path, 'static/profiles', picture_fn)
    print(file_path)
    a = pred_cot_dieas(cottplant = file_path)
    crop_data = disease_solution.crop(a)
    context = {
        "image1": crop_data[0],
        "image2": crop_data[1],
        "image3": crop_data[2],
        "details": crop_data[3],
        "info1": crop_data[4],
        "info2": crop_data[5],
        "info3": crop_data[6],
        "price1": crop_data[7],
        "price2": crop_data[8],
        "price3": crop_data[9],

    }

    file_path1 = url_for('static', filename='user uploaded/' + filename)
    #a = 0
    # print(file_path1)
    # a = pred_cot_dieas(file_path1)
    if current_user.is_authenticated:
        image_file1 = url_for('static', filename='profiles/' + current_user.image_file)
        # print(image_file1)
        abc = filename
        return render_template('cropai.html', image_file=image_file1, user_image=file_path1, pred_output = a,context=context)
    else:
        return render_template('cropai.html', user_image=file_path1, pred_output = a,context=context)


