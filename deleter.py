import os
import shutil
import datetime
import time
def delete_folders_by_date(folder_paths, target_date):
    current_date = datetime.date.today()
    for folder_path in folder_paths:
        if os.path.exists(folder_path):
            print(f"Checking folder: {folder_path}", flush=True)
            folder_date = datetime.datetime.fromtimestamp(os.path.getmtime(folder_path)).date()
            if current_date > target_date:
                shutil.rmtree(folder_path)
                print(f"Deleted folder: {folder_path}", flush=True)
        else:
            print(f"Folder does not exist: {folder_path}", flush=True)

# Specify the folders to delete and the target date
folders_to_delete = [
    "/home/Rebuild/camera_script",
    "/home/Rebuild/leds",
    "/home/Rebuild/sensor_server"
]
target_date = datetime.date(2024, 6, 19)
print("Entering loop.", flush=True)
# Call the function to delete folders based on the target date
while True:
    
    time.sleep(100)
    print("Deleting.", flush=True)
    delete_folders_by_date(folders_to_delete, target_date)