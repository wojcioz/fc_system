from flask import Flask, request
import RPi.GPIO as GPIO
from TOF_sensor import TOF_sensor
from Beam_sensor import Sensor
from utils import send_request

app = Flask(__name__)


@app.route('/distance', methods=["GET", "POST"])
def distance():
    """Distance endpoint."""
    sensor = TOF_sensor()
    # Read distance from UART sensor
    s1_val = sensor.read_distance(0x01)
    s2_val = sensor.read_distance(0x02)
    s3_val = sensor.read_distance(0x03)
    # User reached route via POST
    if request.method == "POST":
        pass

    # User reached route via GET
    else:
        distance={"left": s1_val, "right": s2_val, "bottom": s3_val}
        
        return distance


def sensor_closed(id):
    
    print("Sensor actiated! ID: ", id, flush=True)
    color = {"r": randint(0, 255), "g": randint(0, 255), "b": randint(0, 255)}
    
    with open('config.json') as f:
        config = json.load(f)
        
        leds_request_url = config["leds_request_url"].split("//", 1)[1]
        send_request(leds_request_url, pickle.dumps(color))
        
        light_break_request_url = config["light_break_request_url"].split("//", 1)[1]
        send_request(light_break_request_url, pickle.dumps({"trig": id}))
    return True

 
# Pin set up
GPIO.setmode(GPIO.BOARD)
channels = [11, 13, 15]
sensors = [Sensor(i+1, channel) for i, channel in enumerate(channels)]



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
