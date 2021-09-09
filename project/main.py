from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Camera

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    cameras = Camera.query.filter_by(user_id=current_user.id)
    return render_template('profile.html', name=current_user.name, cameras=cameras)
