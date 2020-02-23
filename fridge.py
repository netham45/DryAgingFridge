#!/usr/bin/python3
import board
import busio
import RPi.GPIO as GPIO
import adafruit_bme680
import time
import graphyte 
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
GPIO.setup(24,GPIO.OUT)
fridgestate = False
HOST="192.168.0.181"
graphyte.init(HOST, prefix='dryage', interval=10)
GPIO.output(24,0)
temppos=0
temps=[2.6,2.6,2.6,2.6,2.6]
onetwentytemps=[2.6] * 10
onetwentytemppos=0
def sleeptime(sltime):
                print("Sleep Thirty")
                for x in range(0,sltime):
                                time.sleep(1)
                                graphyte.send('fridgestate',int(fridgestate))
                                print("{}...".format(x),end='')
while 1:
                curtemp = sensor.temperature
                prevavgtemp=sum(temps)/len(temps)
                temppos=(temppos + 1) % 5
                onetwentytemppos = (onetwentytemppos + 1) % 10
                onetwentytemps[onetwentytemppos] = curtemp
                temps[temppos] = curtemp
                avgtemp=sum(temps)/len(temps)
                onetwentyavgtemp=sum(onetwentytemps)/len(onetwentytemps)
                if abs(curtemp - prevavgtemp) > 5:
                        print("Discarding entry {} - variance > 5".format(curtemp))
                        time.sleep(1)
                        continue
                temppos=(temppos + 1) % 5
                print('Temperature: {}C Average Last 5: {}C Average Last 10: {}C fridgestate: {}'.format(temps[temppos],avgtemp,onetwentyavgtemp,fridgestate))
                if fridgestate:
                        if (avgtemp < 2.65 and avgtemp < onetwentyavgtemp) or avgtemp < 2.35:
                                print("Turning Fridge Off")
                                GPIO.output(24,0)
                                fridgestate = False
                                graphyte.send('fridgestate', int(fridgestate))
                                #time.sleep(30)
                                sleeptime(15)
                if not fridgestate:
                        if (avgtemp > 2.35 and avgtemp > onetwentyavgtemp) or avgtemp > 2.65:
                                print("Turning Fridge On")
                                GPIO.output(24,1)
                                fridgestate = True
                                graphyte.send('fridgestate', int(fridgestate))
                                #time.sleep(30)
                                sleeptime(45)
                graphyte.send('fridgestate', int(fridgestate))
                time.sleep(1)
