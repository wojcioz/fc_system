import RPi.GPIO as GPIO
import json
# import socket
import pickle
from random import randint
from utils import send_request

class Sensor:
    def __init__(self, id, channel):
        self.id = id
        self.channel = channel
        GPIO.setup(self.channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.channel, GPIO.RISING, callback=self.sensor_activated)

    def sensor_activated(self, channel):
        # {
        #     "effect": "breathe",
        #     "parameters": [1, 10],
        #     "color": [255, 255, 255]
        # }
        print(f"Sensor {self.id} activated on channel {channel}")
        print("Sensor activated! ID: ", id, flush=True)
        color = {"r": randint(0, 255), "g": randint(0, 255), "b": randint(0, 255)}
        
        with open('config.json') as f:
            config = json.load(f)
            
            leds_request_url = config["leds_request_url"].split("//", 1)[1]
            send_request(leds_request_url, pickle.dumps(color))
            
            light_break_request_url = config["light_break_request_url"].split("//", 1)[1]
            send_request(light_break_request_url, pickle.dumps({"trig": id}))
        return True
