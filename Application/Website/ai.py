import os

from flask import flash, Blueprint, Flask, render_template, request, session, Response, current_app
from .models import imageTracker
from . import db
from flask_login import current_user
from keras.models import load_model
import keras.utils as image
from werkzeug.utils import secure_filename

ai = Blueprint('ai', __name__)

dic = {0 : 'Recylcable', 1 : 'Organic'}

model = load_model('/Users/larissasmith/Projects/Wecycle/Application/Website/static/model/my_model.h5')

model.make_predict_function()

def classifyLabel(img_path):
    i = image.load_img(img_path, target_size=(224, 224))
    i = image.img_to_array(i)/255.0
    i = i.reshape(1, 224, 224, 3)
    p = (model.predict(i) > 0.5).astype("int32")
    return dic[p[0][0]]

@ai.route('/scan')
def scan():
    return render_template('scan.html', user=current_user)
@ai.route("/scan", methods = ['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        img = request.files['uploaded-file']
        if img:
            if current_user.is_authenticated:
                tracking_entry = imageTracker(user_id=current_user.id) #Adding a saved tracker id into the database that correlates to the user id
                db.session.add(tracking_entry)
                db.session.commit()
                flash('Your Tracker Has Been Updated!')
            img_filename = secure_filename(img.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']

            saved_img_path = os.path.join(upload_folder, img_filename)
            img.save(saved_img_path)
            img_path = os.path.join('static/uploads', img_filename)

            session['uploaded_img_file_path'] = img_path
            p = classifyLabel(saved_img_path)
            return render_template("scan2.html", prediction=p, img_path=img_path, user=current_user)
        else:
            return render_template("scan2.html", user=current_user)

# @ai.route('/scan')
# def scan():
#     return render_template('scan.html', user=current_user)
#
# #Take image file if submit is clicked, open scan2
# @ai.route('/scan', methods=("POST", "GET"))
# def uploadFile():
#     if request.method == 'POST':
#         # Extracting uploaded file and passing it to scan2
#         uploaded_img = request.files['uploaded-file']
#         img_filename = secure_filename(uploaded_img.filename)
#         uploaded_img.save(os.path.join(current_app.config['UPLOAD_FOLDER'], img_filename))
#
#         session['uploaded_img_file_path'] = os.path.join(current_app.config['UPLOAD_FOLDER'], img_filename)
#
#     img_file_path = session.get('uploaded_img_file_path', None)
#
#     return render_template('scan2.html', user_image=img_file_path, user=current_user)
