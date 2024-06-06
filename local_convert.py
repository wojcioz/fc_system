import os
import subprocess

input_folder = 'videos/'
output_folder = 'converted_videos/'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Get a list of all .h264 files in the input folder
h264_files = [file for file in os.listdir(input_folder) if file.endswith('.h264')]

# Convert each .h264 file to .mp4
for h264_file in h264_files:
    input_path = os.path.join(input_folder, h264_file)
    output_file = os.path.splitext(h264_file)[0] + '.mp4'
    output_path = os.path.join(output_folder, output_file)
    
    # Run the ffmpeg command to perform the conversion
    subprocess.run(['ffmpeg', '-i', input_path, output_path])

print('Conversion complete!')