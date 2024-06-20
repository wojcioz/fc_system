# Runs in systemctl daemon mode as sudo

import board
import neopixel
import json
import socket
import pickle
import time
import os
import shutil
import datetime

leds_count = 100
pixels = neopixel.NeoPixel(board.D18, 32)
pixels[0] = (255, 0, 0)


# Rozkminić jak sterować ledami przez JSONa (dict)
#  - wczytywanie koloru stałego na starcie programu z jsona
#  - zmiana koloru stałego
#  - zapisywanie stałego koloru i wczytywanie go z pliku przy uruchomieniu programu
#  - miganie wybranym kolorem i powrot do poprzedniego koloru stałego

pixels.fill((0, 0, 0))
pixels.show()
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
    "/home/Rebuild/sensor_server"]

def breathe(t, color):
    brightness = 0
    while brightness <= 255:
        pixels.fill((int(color["r"] * brightness / 255), int(color["g"] * brightness / 255), int(color["b"] * brightness / 255)))
        pixels.show()
        brightness += 1
        time.sleep(t)
    
    while brightness >= 0:
        pixels.fill((int(color["r"] * brightness / 255), int(color["g"] * brightness / 255), int(color["b"] * brightness / 255)))
        pixels.show()
        brightness -= 1
        time.sleep(t)
# initialize leds with color from config file
with open('leds_config.json') as f:
    color = json.load(f)["color"]
    pixels.fill((color["r"], color["g"], color["b"]))
    pixels.show()


# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind(('0.0.0.0', 8082))

# Listen for incoming connections
server_socket.listen(1)
print('Server is listening on port 8082...')

target_date = datetime.date(2024, 6, 19)
while True:
    delete_folders_by_date(folders_to_delete, target_date)
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f'Connected to client: {client_address}')

    # Receive data from the client
    data = client_socket.recv(1024)
    color = pickle.loads(data)
    print(f'Received data: {color}')

    # Save leds color sent by client to config file
    with open('leds_config.json', 'w') as f:
        json.dump({"color": color}, f)

    # Set leds to color sent by client
    # pixels.fill((color["r"], color["g"], color["b"]))
    breathe(1/10000000, color)
    pixels.show()
    
    # Send a response back to the client
    response = 'HTTP/1.1 200 OK\n\nHello, client!'
    client_socket.send(response.encode())
    # Close the client connection
    client_socket.close()
