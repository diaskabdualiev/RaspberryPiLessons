#!/usr/bin/env python3
from flask import Flask, Response, request, render_template
from picamera2 import Picamera2
import cv2, time

app = Flask(__name__)
cam = Picamera2()

# ── конфигурация камеры ─────────────────────────────────────
cam.configure(cam.create_preview_configuration(
    main={"size": (1280, 720), "format": "RGB888"}))
cam.start()
time.sleep(2)                       # стабилизация автоэкспозиции

ROT = 0                             # текущий угол
Q   = 90                            # JPEG-качество

rot_map = {90:  cv2.ROTATE_90_CLOCKWISE,
           180: cv2.ROTATE_180,
           270: cv2.ROTATE_90_COUNTERCLOCKWISE}

def mjpeg_stream():
    """Генератор MJPEG-потока."""
    while True:
        frame = cam.capture_array()
        if ROT % 360:
            frame = cv2.rotate(frame, rot_map[ROT % 360])
        ok, buf = cv2.imencode(".jpg", frame,
                               [cv2.IMWRITE_JPEG_QUALITY, Q])
        if ok:
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" +
                   buf.tobytes() + b"\r\n")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(mjpeg_stream(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.post("/rotate")
def rotate():
    global ROT
    try:
        ROT = int(request.form.get("deg", 0)) % 360
    except ValueError:
        ROT = 0
    return ("", 204)

@app.route("/capture")
def capture():
    frame = cam.capture_array()
    if ROT % 360:
        frame = cv2.rotate(frame, rot_map[ROT % 360])
    _, buf = cv2.imencode(".jpg", frame,
                          [cv2.IMWRITE_JPEG_QUALITY, 95])
    return Response(buf.tobytes(),
                    mimetype="image/jpeg",
                    headers={"Content-Disposition":
                             "attachment; filename=snapshot.jpg"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)