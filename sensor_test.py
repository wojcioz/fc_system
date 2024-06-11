# coding: UTF-8

# This code is supposed to control 3 UART sensors (distance) and 3 DI sensors (light break).
import RPi.GPIO as GPIO
import serial
import time
import chardet
import struct
import sys
import requests

TOF_length = 16
TOF_header = (87, 0, 255)
TOF_system_time = 0
TOF_distance = 0
TOF_status = 0
TOF_signal = 0
TOF_check = 0


def verifyCheckSum(data, len):
    # print(data)
    TOF_check = 0
    for k in range(0, len - 1):
        TOF_check += data[k]
    TOF_check = TOF_check % 256
    if TOF_check == data[len - 1]:
        print("TOF data is ok!")
        return 1
    else:
        print("TOF data is error!")
        return 0


def calcCheckSum(data, len):
    TOF_check = 0
    for k in range(0, len):  # NIE MA len-1 jak w verifyCheckSum
        TOF_check += data[k]
    TOF_check = TOF_check % 256
    return TOF_check

##17 27 22
# TODO Change the code to run on a flask server and respond with all 3 distances on endpoint /distance. format output to [x,y,z]
# TODO When one of the DI sensors is activated, a request is to be send to address form config file.
# ktos wchodzi na endpoint /distance i wtedy wysylany jest request do serwera z config.json z informacja o przerwaniu wiazki.

# Pin set up
GPIO.setmode(GPIO.BOARD)
channels = [11, 13, 15]
for channel in channels:
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(channel, GPIO.RISING)  # add rising edge detection on a channel


SENSOR_ID = 0x02

RAW_QUERY = (0x57, 0x10, 0xFF, 0xFF, SENSOR_ID, 0xFF, 0xFF)
RAW_QUERY += (calcCheckSum(RAW_QUERY, len(RAW_QUERY)),)
print(f"RAW_QUERY: {RAW_QUERY}")

ser = serial.Serial("/dev/ttyS0", 115200)
ser.flushInput()

while True:

    # Wysalnie  zapytania
    ser.write(bytes(RAW_QUERY))
    # print(f"Wyslano zapytanie po uarcie o tresci {bytes(RAW_QUERY)}")
    time.sleep(1)

    # czekanie na napelnienie bufora
    print(f"{ser.inWaiting()} bajtow czeka w buforze uart")
    if ser.inWaiting() >= 16:

        # sczytanie danych z bufora
        TOF_data = ()
        for i in range(0, 16):
            TOF_data = TOF_data + (ord(ser.read(1)),)

        # sprawdznie poprawnosci naglowka i sumy kontrolnej
        if (
            TOF_data[0] == TOF_header[0]
            and TOF_data[1] == TOF_header[1]
            and TOF_data[2] == TOF_header[2]
        ) and (verifyCheckSum(TOF_data[:TOF_length], TOF_length)):
            if ((TOF_data[12]) | (TOF_data[13] << 8)) == 0:
                print("Out of range!")
            else:
                print("TOF id is: " + str(TOF_data[3]))
                TOF_system_time = (
                    TOF_data[4]
                    | TOF_data[5] << 8
                    | TOF_data[6] << 16
                    | TOF_data[7] << 24
                )
                print("TOF system time is: " + str(TOF_system_time) + "ms")
                TOF_distance = (TOF_data[8]) | (TOF_data[9] << 8) | (TOF_data[10] << 16)
                print("TOF distance is: " + str(TOF_distance) + "mm")
                TOF_status = TOF_data[11]
                print("TOF status is: " + str(TOF_status))
                TOF_signal = TOF_data[12] | TOF_data[13] << 8
                print("TOF signal is: " + str(TOF_signal))

    else:
        print("Nie ma odpowiedzi")
        
    # for channel in channels:
    #     if GPIO.event_detected(channel):
    #         print(f"Sensor {channel} activated")
    #         requests.get("http://127.0.0.1:8000/distance")
