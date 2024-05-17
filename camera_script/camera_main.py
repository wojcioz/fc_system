from flask import Flask, Response, send_from_directory
import time
from CameraHandler import CameraHandler
import os
app = Flask(__name__)

        

@app.route("/video_feed")
def video_feed():
    global cam_handler
    return Response(
        cam_handler.get_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/start_capture")
def start_capture():
    global cam_handler
    cam_handler.start_recording()
    return "Capture started"

@app.route("/stop_capture")
def stop_capture():
    global cam_handler
    cam_handler.stop_recording()
    return "Capture stopped"

@app.route("/convert")
def convert():
    global cam_handler
    cam_handler.convert_vids()
    return "Conversion started"

@app.route('/files', defaults={'req_path': ''})
@app.route('/files/<path:req_path>')
def dir_listing(req_path):
    BASE_DIR = '/home/Rebuild/recs'
    abs_path = os.path.join(BASE_DIR, req_path)
    if not os.path.exists(abs_path):
        return "Not Found", 404
    if os.path.isfile(abs_path):
        return send_from_directory(BASE_DIR, req_path)
    files = os.listdir(abs_path)
    return "<br>".join(files)


global cam_handler 
cam_handler = CameraHandler()

cap_single_vid = False

if cap_single_vid:
    print("Starting recording")
    cam_handler.start_recording()
    print("waiting 10s")
    time.sleep(10)
    cam_handler.stop_recording()
    print("Record done")
else:
    if __name__ == "__main__":
        app.run(
            host="0.0.0.0", port="5000"
        ) 
