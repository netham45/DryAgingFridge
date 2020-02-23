#!/usr/bin/python3
import board
import busio
import RPi.GPIO as GPIO
import adafruit_bme680
import time
import graphyte 
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
GPIO.setup(25,GPIO.OUT)
fanstate = False
oob = False
HOST="192.168.0.181"
graphyte.init(HOST, prefix='dryage', interval=10)
GPIO.output(25,0)
humidities=[-1] * 15
humiditiespos=0

def avg(arr):
    count = 0
    total = 0
    for ele in arr:
        if not ele == -1:
            total = total + ele
            count = count + 1
    if count == 0:
        return -1
    return total / count

while 1:
    print('Humidity: {}%'.format(sensor.humidity))
    curhumid = sensor.humidity
    humiditiespos = (humiditiespos + 1) % 15
    humidities[humiditiespos] = curhumid
    if ( abs(curhumid-avg(humidities)) > 15 ):
        print("Bad value - discarding")
        time.sleep(1)
        continue
            
    if sensor.humidity < 77.5:
        if not fanstate:
            print("Turning Fan On")
            GPIO.output(25,1)
            fanstate = True
    if sensor.humidity > 79.5:
        if fanstate:
            print("Turning Fan Off")
            GPIO.output(25,0)
            fanstate = False
    graphyte.send('fanstate', int(fanstate))
    time.sleep(1
