import os
import time
import cv2
from datetime import datetime

def generate_filename(format):
    # Generates a folder with current date, and path to the file that 
    # is current time, as an arguments it takes file extension and names
    # the output path accordingly
    filename = os.path.join(
        "/home/Rebuild/recs", time.strftime("%Y%m%d"), time.strftime("%H%M%S") + format
    )
    folder_path = os.path.dirname(filename)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return filename


def convert_videos(input_folder):
    # Create a new folder for converted videos
    
    start_time = datetime.now()
    output_folder = os.path.join(input_folder, "converted_videos")
    os.makedirs(output_folder, exist_ok=True)
    print(input_folder)
    # Get a list of all .h264 files in the input folder
    video_files = [f for f in os.listdir(input_folder) if f.endswith(".h264")]
    print(video_files)
    for video_file in video_files:
        print("Processing file: ", video_file)
        # Construct the input and output file paths
        input_path = os.path.join(input_folder, video_file)
        output_path = os.path.join(output_folder, video_file.replace(".h264", ".avi"))

        # Read the input video using OpenCV
        video = cv2.VideoCapture(input_path)

        # Get the video properties
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = video.get(cv2.CAP_PROP_FPS)

        # Create a VideoWriter object to write the converted video
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while True:
            # Read a frame from the input video
            ret, frame = video.read()

            if not ret:
                break

            # Write the frame to the output video
            writer.write(frame)

        # Release the video objects
        video.release()
        writer.release()
    print("Conversion took:", (datetime.now() - start_time).total_seconds())
    print("Videos converted successfully!")
    
    
class RingBuffer:
    """ class that implements a not-yet-full buffer """
    def __init__(self,size_max):
        self.max = size_max
        self.data = []

    class __FullRingBuffer:
        "Class that implements a full buffer, RingBuffer morphs to this when full"
        def append(self, x):
            """ Append an element overwriting the oldest one. """
            self.data[self.cur] = x
            self.cur = (self.cur+1) % self.max
        def get(self):
            """ return list of elements in correct order """
            return self.data[self.cur:]+self.data[:self.cur]
        def get_oldest(self):
            return self.data[(self.cur+1)% self.max]
    def append(self,x):
        """append an element at the end of the buffer"""
        self.data.append(x)
        if len(self.data) == self.max:
            self.cur = 0
            # Permanently change self's class from non-full to full
            self.__class__ = self.__FullRingBuffer

    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        return self.data
    def get_oldest(self):
        return self.data[self.cur+1]