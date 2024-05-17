from picamera2 import MappedArray, Picamera2, Preview
from libcamera import controls
from picamera2.encoders import H264Encoder, Quality

from utils import generate_filename, convert_videos, RingBuffer
import threading
import time
import queue
import cv2

class FrameReader(RingBuffer):    
    def __init__(self):
        self.max = 2
        self.data = []
        self.cur = 0
    def read(self):
        """ Return a list of elements from the newest to the oldest. """
        return self.data[self.cur+1]
    def write(self,frame):
        self.append(frame)



class CameraHandler:
    def __init__(self):
        self.cam = Picamera2()
        self.cam.configure(
            self.cam.create_video_configuration(main={"size": (1920, 1080),"format": "RGB888"},
                                                  lores={"size": (1280, 720),"format": "YUV420"})
        )
        self.mode = "lores"
        self.cam.set_controls({"AfMode": controls.AfModeEnum.Continuous, "FrameRate": 20})
        self.recording = False
        self.encoder = H264Encoder(10000000)
        self.thread = None
        self.frame_reader = RingBuffer(size_max=2)
        
    def start_recording(self):
        print(generate_filename(".h264"))
        self.cam.start_recording(self.encoder, generate_filename(".h264"),name=self.mode, quality=Quality.MEDIUM)
        print("Recording started")
        self.recording = True
        self.thread = threading.Thread(target=self._generate_frames)
        self.thread.start()
        
    def stop_recording(self):
        self.cam.stop_recording()
        print("Recording paused")
        self.recording = False
        if self.thread is not None:
            self.thread.join()
            
    def convert_vids(self):
        convert_videos("recs/20240416")
        
    def _generate_frames(self):
        while True:
            time.sleep(1.0/10.0)
            try:
                if not self.recording:
                    break
                array = self.cam.capture_array()
                
                self.frame_reader.append(array)
                
            except Exception as e:
                print(f"Error: {e}")
    
    
    def get_frames(self):
        while True:
            array = self.frame_reader.get_oldest()
            _, jpeg = cv2.imencode('.jpg', array)
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            if self.recording == False:
                break
        
