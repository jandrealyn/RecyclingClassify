# Laras code for rendering html files

from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


# Shows welcome page
@views.route('/')
def welcome():
    return render_template('welcome.html', user=current_user)

# Tracker page which only shows a tree at the moment
@views.route('/tracker')
def tracker():
    return render_template('tracker.html', user=current_user)
