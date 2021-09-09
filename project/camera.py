from flask import Blueprint, render_template, Response, request, send_from_directory
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from .stream_camera import gen_frames, test_camera_with_requests
from .models import Camera
from . import db


camera = Blueprint('camera', __name__)


@camera.route('/stream')
@login_required
def stream():
    id = request.args.get('camera_id')
    founded_camera = Camera.query.get(id)
    return render_template('stream.html', camera=founded_camera)


@camera.route('/video_feed')
@login_required
def video_feed():
    id = request.args.get('camera_id')
    print(id)
    founded_camera = Camera.query.get(id)
    test_camera_result = test_camera_with_requests(founded_camera.test_url)
    if(test_camera_result):
        return Response(gen_frames(founded_camera.video_url), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return send_from_directory('statics/images', 'camera_offline.png')


@camera.route('/test_camera')
@login_required
def test_camera():
    id = request.args.get('camera_id')
    founded_camera = Camera.query.get(id)
    test_camera_result = test_camera_with_requests(founded_camera.test_url)
    if(test_camera_result):
        return send_from_directory('statics/images', 'camera_online.jpg')
    else:
        return send_from_directory('statics/images', 'camera_offline.png')


@camera.route('/see_all_camera')
@login_required
def see_all_camera():
    cameras = Camera.query.filter_by(user_id=current_user.id)
    return render_template('camera_list.html', cameras=cameras)


@camera.route('/add_camera', methods=['GET'])
@login_required
def add_camera():
    return render_template('add_camera.html')


@camera.route('/add_camera_post', methods=['POST'])
@login_required
def add_camera_post():
    name = request.form.get('name')
    video_url = request.form.get('video_url')
    audio_url = request.form.get('audio_url')
    test_url = request.form.get('test_url')
    test_camera_result = test_camera_with_requests(test_url)
#
    if(test_camera_result):
        new_camera = Camera(name=name, video_url=video_url,
                            audio_url=audio_url, test_url=test_url, user_id=current_user.id)
        db.session.add(new_camera)
        db.session.commit()

    return redirect(url_for('camera.see_all_camera'))


@camera.route('/delete_camera')
@login_required
def delete_camera():
    id = request.args.get('camera_id')
    print(id)
    fetched_camera = Camera.query.get(id)
    if(fetched_camera.user_id == current_user.id):
        db.session.delete(fetched_camera)
        db.session.commit()
        print(f'Camera {fetched_camera.id} name={fetched_camera.name} deleted')
    return redirect(url_for('camera.see_all_camera'))
