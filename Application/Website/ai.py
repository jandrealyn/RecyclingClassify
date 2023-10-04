from flask import Blueprint, Flask, render_template, request, session, Response
import pandas as pd

from keras.models import load_model
import csv
import os
import cv2
import base64
import json
import pickle
from werkzeug.utils import secure_filename

import cv2
import numpy as np


ai = Blueprint('ai', __name__)


def detect_object(uploaded_image_path):
    model = load_model("static/model/my_model.h5")

    img = cv2.imread(uploaded_image_path)

    label = "static/model/labels.txt"

    predictions = model.predict(img)

    # Draw bounding box with text for each object
    font = cv2.FONT_HERSHEY_DUPLEX
    for prediction in predictions:
        class_id = int(prediction[0])
        confidence = float(prediction[1])
        x = int(prediction[2])
        y = int(prediction[3])
        width = int(prediction[4])
        height = int(prediction[5])

        # Draw bounding box
        cv2.rectangle(img, (x, y), (x + width, y + height), (0, 255, 0), 2)

        # Add label and confidence score
        text = f"{label}: {confidence:.2f}"
        cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Save the output image
    output_image_path = os.path.join(ai.config['UPLOAD_FOLDER'], 'output_image.jpg')
    cv2.imwrite(output_image_path, img)

    return (output_image_path)

# Detect image by passing its image back with detection
@ai.route('/detect_object')
def detectObject():
    uploaded_image_path = session.get('uploaded_img_file_path', None)
    output_image_path = detect_object(uploaded_image_path)
    print(output_image_path)
    return render_template('scan2.html', user_image=output_image_path)

# Solve flask cache images issue
@ai.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
