from flask import Flask, render_template, request
import json
import socket
import struct


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
        return render_template("distance.html", distance=distance)


def sensor_closed(id):
    with open('config.json') as f:
        config = json.load(f)
        light_break_request_url = config["light_break_request_url"].split("//", 1)[1]
        light_break_request_ip = light_break_request_url.split(":", 1)[0]
        light_break_request_port = int(light_break_request_url.split(":", 1)[1])

        try:
            # Create a socket object
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Set a timeout value of 2 seconds
            sock.settimeout(2)
            
            # Attempt to connect to the IP address and port
            result = sock.connect_ex((light_break_request_ip, light_break_request_port))
            
            if result == 0:
                print(f"Connection to {light_break_request_ip}:{light_break_request_port} is successful")
                sock.send(bytes(json.dumps({"trig": id}), encoding="utf-8"))
            else:
                print(f"Connection to {light_break_request_ip}:{light_break_request_port} failed")

            # Close the socket
            sock.close()
        
        except socket.error as e:
            print(f"Error occurred while connecting: {e}")


    return True

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
