import cv2
import requests


def gen_frames(camera_location):
    cam = cv2.VideoCapture(camera_location)
    cam.set(3, 1920)
    cam.set(4, 1080)
    while True:
        success, frame = cam.read()
        frame = cv2.flip(frame, 1)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def test_camera(camera_location):

    print(camera_location)
    try:
        cam = cv2.VideoCapture(camera_location)
        print(cam)
        cam.set(3, 1920)
        cam.set(4, 1080)
        success, frame = cam.read()
        return True
    except cv2.error as e:
        print(e)
        return False


def test_camera_with_requests(camera_location):
    timeout = 5
    try:
        request = requests.get(camera_location, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        print(exception)
        return False
