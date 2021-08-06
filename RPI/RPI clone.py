#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial,time

from serial.serialutil import SerialException

"""
This part is to check which arduino is which by checking through all the ports
"""
checkdone = False #checks if the current check is done
test = True
prevACMport = 0 #previous valid port found the check so there's no duplication
prevUSBport = 0
nports = 1 #number of ports/connections

for port in range(nports):
    #this for loop is for searching through the differently named ports
    for i in range(prevACMport, 10): #ttyACM ver.
        try: 
            arduino1 = serial.Serial("/dev/ttyACM"+str(i), 9600, timeout = 1)
            print("/dev/ttyACM" + str(i)," connected")
            prevACMport = i+1
            break
        except SerialException:
            print("/dev/ttyACM" + str(i), " is not a valid port")

    for i in range(prevUSBport, 10): #ttyUSB ver.
        try:
            arduino1 = serial.Serial("/dev/ttyUSB"+str(i), 9600, timeout = 1)
            print("/dev/ttyUSB" + str(i)," connected")
            prevUSBport = i+1
            break
        except SerialException:
            print("/dev/ttyUSB" + str(i), " is not a valid port")
    try:
        if arduino1.isOpen(): #this loop only starts after the we found a port
            while not checkdone: #keeps checking for input until we have the desired ID phrase
                while arduino1.in_waiting>0: #while there is stuff wating to be received in this "check"
                    try: 
                        answer = arduino1.readline().decode()
                        answer = answer[:-1] #remove the newline behind
                        answer = answer.split()
                        print(answer)
                        if answer[0] == "SENSOR": #assigns the connected arduino to it's correct name
                            checkdone = True
                            arduinoSensor = arduino1
                            print("Sensor found")
                            break
                        elif answer[0] == "MOVEMENT":
                            checkdone = True
                            arduinoMove = arduino1
                            print("Movement found")
                            break
                        elif answer[0] == "CLEAN":
                            checkdone = True
                            arduinoClean = arduino1
                            print("Clean found")
                            break
                        time.sleep(0.01)
                    except:
                        pass
    except NameError:
        print("No Arduino connected")

running = True
while running:
    try:
        while arduinoSensor.in_waiting > 0:
            sensor_vals = arduinoSensor.readline().decode()
            sensor_vals = sensor_vals[:-1]
            sensor_vals = sensor_vals.split()
            print(sensor_vals)
    except KeyboardInterrupt:
        print("\nclosing file")
        arduinoSensor.close()
        running = False
