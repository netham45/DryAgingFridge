#!/usr/bin/env python3

import adafruit_bme680
import board
import busio
from datetime import datetime
from gpiozero import CPUTemperature
import graphyte
import time

HOST = '192.168.0.181' 

graphyte.init(HOST, prefix='dryage')
cpu = CPUTemperature()
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

temps=[-1] * 15
temppos=0
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
    curtemp = sensor.temperature
    curhumid = sensor.humidity
    temppos = (temppos + 1) % 15
    humiditiespos = (humiditiespos + 1) % 15
    temps[temppos] = curtemp
    humidities[humiditiespos] = curhumid
    if ( abs(curtemp-avg(temps)) > 5 or abs(curhumid-avg(humidities)) > 25 ):
        time.sleep(1)
        continue
    print("CPU Temp: {} Sensor Temp: {}".format(cpu.temperature,sensor.temperature))
    print("Humidity: {}".format(sensor.humidity))
    print("Gas: {} Pressure: {}".format(sensor.gas,sensor.pressure))
    graphyte.send('picputemp', cpu.temperature)
    graphyte.send('temperature',sensor.temperature)
    graphyte.send('gas',sensor.gas)
    graphyte.send('humidity',sensor.humidity)
    graphyte.send('pressure',sensor.pressure)
    time.sleep(1)
