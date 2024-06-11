import serial
import time

import RPi.GPIO as GPIO

class TOF_sensor:
    def __init__(self):
        # Initialize GPIO and serial communication here
        self.TOF_length = 16
        self.TOF_header = (87, 0, 255)
        self.TOF_system_time = 0
        self.TOF_distance = 0
        self.TOF_status = 0
        self.TOF_signal = 0
        self.TOF_check = 0
        pass

    def read_distance(self, sensor_id):
        
        SENSOR_ID = sensor_id

        RAW_QUERY = (0x57, 0x10, 0xFF, 0xFF, SENSOR_ID, 0xFF, 0xFF)
        RAW_QUERY += (self.calcCheckSum(RAW_QUERY, len(RAW_QUERY)),)
        print(f"RAW_QUERY: {RAW_QUERY}")

        ser = serial.Serial("/dev/ttyS0", 115200)
        ser.flushInput()
        
        while True:
            ser.write(bytes(RAW_QUERY))
            print(f"{ser.inWaiting()} bajtow czeka w buforze uart")
            
            if ser.inWaiting() >= 16:

                # sczytanie danych z bufora
                TOF_data = ()
                for i in range(0, 16):
                    TOF_data = TOF_data + (ord(ser.read(1)),)

                # sprawdznie poprawnosci naglowka i sumy kontrolnej
                if (
                    TOF_data[0] == self.TOF_header[0]
                    and TOF_data[1] == self.TOF_header[1]
                    and TOF_data[2] == self.TOF_header[2]
                ) and (self.verifyCheckSum(TOF_data[:self.TOF_length], self.TOF_length)):
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
                        return TOF_distance
            else:
                print("Nie ma odpowiedzi")
                return "NO DATA"
        
        
    def cleanup(self):
        # Clean up GPIO and serial communication here
        pass
    
    def verifyCheckSum(self, data, len):
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
    def calcCheckSum(self, data, len):
        TOF_check = 0
        for k in range(0, len):  # NIE MA len-1 jak w verifyCheckSum
            TOF_check += data[k]
        TOF_check = TOF_check % 256
        return TOF_check