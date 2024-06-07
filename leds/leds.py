# Runs in systemctl daemon mode as sudo

import board
import neopixel
import json
import socket
import pickle


pixels = neopixel.NeoPixel(board.D18, 30)
pixels[0] = (255, 0, 0)

leds_count = 100
# Rozkminić jak sterować ledami przez JSONa (dict)
#  - wczytywanie koloru stałego na starcie programu z jsona
#  - zmiana koloru stałego
#  - zapisywanie stałego koloru i wczytywanie go z pliku przy uruchomieniu programu
#  - miganie wybranym kolorem i powrot do poprzedniego koloru stałego

pixels.fill((0, 0, 0))
pixels.show()

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

while True:
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
    pixels.fill((color["r"], color["g"], color["b"]))
    pixels.show()
    
    # Send a response back to the client
    response = 'HTTP/1.1 200 OK\n\nHello, client!'
    client_socket.send(response.encode())
    # Close the client connection
    client_socket.close()
