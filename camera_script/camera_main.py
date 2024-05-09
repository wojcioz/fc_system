from flask import Flask, Response
import cv2
import numpy as np
import time
from CameraHandler import CameraHandler

app = Flask(__name__)

        
def generate_frames():
    global cam_handler
    # time.sleep(0.1)  # allow the camera to warmup
    encoder = H264Encoder(10000000)
    while True:
        time.sleep(0.1)
        if not cam_handler.recording:
            break
        try:
            # array = cam_handler.cam.capture_array()
            # cam_handler.cam.start_recording(encoder, 'test.h264')
            # _, jpeg = cv2.imencode('.jpg', array)
            # yield (b'--frame\r\n'
            #        b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            if not cam_handler.recording:
                break
        except Exception as e:
            print(f"Error: {e}")
            continue
    cam_handler.cam.stop_recording()
    print("Stopping frame generation")        

@app.route("/video_feed")
def video_feed():
    global cam_handler
    return Response(
        cam_handler.get_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/start_capture")
def start_capture():
    global cam_handler
    # cam_handler.start()
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
        )  # host and port can be changed as per requirement
