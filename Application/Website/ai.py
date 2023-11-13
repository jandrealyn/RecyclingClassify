import os
import tempfile
from flask import flash, Blueprint, Flask, render_template, request, session, Response, current_app
from .models import imageTracker
from . import db
from flask_login import current_user
from keras.models import load_model
import keras.utils as image
from werkzeug.utils import secure_filename, redirect


ai = Blueprint('ai', __name__)

dic = {0 : 'Recyclable', 1 : 'Organic'}

model = load_model('/Users/larissasmith/Projects/Wecycle/Application/Website/static/model/my_model.h5')

model.make_predict_function()

def classifyLabel(img_path): #Keras is utilised in loading and preprocessing the image for the model
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
            if current_user.is_authenticated: #Only create tracker or add to tracker if user has an account
                existing_tracker = imageTracker.query.filter_by(user_id=current_user.id).first()

                if existing_tracker:
                    existing_tracker.increment_counter()
                else:
                    tracking_entry = imageTracker(user_id=current_user.id)  # Adding a saved tracker id into the database that correlates to the user id
                    db.session.add(tracking_entry)

                db.session.commit()
                flash('Your Tracker Has Been Updated!')

            if 'uploaded_img_file_path' in session: #Checking if user has already uploaded an image to scan
                previous_img_path = session['uploaded_img_file_path'] #We are taking the web version of file name
                img_filename = os.path.basename(previous_img_path)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                accessible_img_path = os.path.join(upload_folder, img_filename) #Converted it to base, and added back the local parts of the file name to properly find it
                if os.path.exists(accessible_img_path):
                    print(f"Previous image removed: {previous_img_path}")
                    os.remove(accessible_img_path) #Delete it if it exists

            img_filename = secure_filename(img.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']

            saved_img_path = os.path.join(upload_folder, img_filename)
            img.save(saved_img_path)
            img_path = os.path.join('static/uploads', img_filename)   #The saved img path is seperate from the path that gets uploaded for the user to see

            session['uploaded_img_file_path'] = img_path
            p = classifyLabel(saved_img_path)
            return render_template("scan2.html", prediction=p, img_path=img_path, user=current_user)
        else:
            return render_template("scan2.html", user=current_user)

@ai.route("/scan2")
def resetScan():
    return render_template("scan.html", user=current_user)