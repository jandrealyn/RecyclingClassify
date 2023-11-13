# Laras code for rendering html files

from .models import imageTracker
from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

# Shows welcome page
@views.route('/')
def welcome():
    return render_template('welcome.html', user=current_user)

@views.route('/tracker')
def tracker():
    # Retrieve the imageTracker instance associated with the user
    tracker = imageTracker.query.filter_by(user_id=current_user.id).first()
    if tracker:
        counter = tracker.counter
    else:
        counter = 0

    return render_template('tracker.html', counter=counter, user=current_user)
