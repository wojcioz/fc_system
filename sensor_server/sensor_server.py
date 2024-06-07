from flask import Flask, request
import json
import socket
import pickle
from random import randint


app = Flask(__name__)


@app.route('/distance', methods=["GET", "POST"])
def distance():
    """Distance endpoint."""

    # User reached route via POST
    if request.method == "POST":
        pass

    # User reached route via GET
    else:
        distance={"left": 3.4, "right": 8, "bottom": 12.7}
        sensor_closed(1)
        return distance


def sensor_closed(id):
    # {
    #     "effect": "breathe",
    #     "parameters": [1, 10],
    #     "color": [255, 255, 255]
    # }
    color = {"r": randint(0, 255), "g": randint(0, 255), "b": randint(0, 255)}
    
    with open('config.json') as f:
        config = json.load(f)
        
        leds_request_url = config["leds_request_url"].split("//", 1)[1]
        send_request(leds_request_url, pickle.dumps(color))
        
        light_break_request_url = config["light_break_request_url"].split("//", 1)[1]
        send_request(light_break_request_url, pickle.dumps({"trig": id}))
    return True

def send_request(url, data):
    ip = url.split(":", 1)[0]
    port = int(url.split(":", 1)[1])
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a timeout value of 2 seconds
        sock.settimeout(2)
        
        # Attempt to connect to the IP address and port
        result = sock.connect_ex((ip, port))
        
        if result == 0:
            print(f"Connection to {ip}:{port} is successful")
            sock.send(data)
        else:
            print(f"Connection to {ip}:{port} failed")

        # Close the socket
        sock.close()
    
    except socket.error as e:
        print(f"Error occurred while connecting: {e}")
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
