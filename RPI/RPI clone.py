#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial,time
import mapping as Map
from serial.serialutil import SerialException

"""
This part is to check which arduino is which by checking through all the ports
"""
checkdone = False #checks if the current check is done
test = True
prevACMport = 0 #previous valid port found the check so there's no duplication
prevUSBport = 0
nports = 2 #number of ports/connections
missingArduino = True

while missingArduino: 
    for port in range(nports):
        #this for loop is for searching through the differently named ports
        for i in range(prevACMport, 10): #ttyACM ver.
            try: 
                arduino1 = serial.Serial("/dev/ttyACM"+str(i), 9600, timeout = 1)
                print("/dev/ttyACM" + str(i)," connected")
                prevACMport = i+1
                connected = True
                break
            except SerialException:
                print("/dev/ttyACM" + str(i), " is not a valid port")
        if not connected:
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
                                # break
                            elif answer[0] == "MOVEMENT":
                                checkdone = True
                                arduinoMove = arduino1
                                print("Movement found")
                                # break
                            elif answer[0] == "PUMP":
                                checkdone = True
                                arduinoPump = arduino1
                                print("PUMP found")
                                # break
                            connected = False
                            time.sleep(0.01)
                        except:
                            pass
            checkdone = False
        except NameError:
            print("No Arduino connected")
    #This is to check that all required components are connected
    try:
        print(arduinoSensor)
        print(arduinoMove)
        print(arduinoPump)
        missingArduino = False
    except:
        continue


"""
Format is going to be:
1. Read information from sensor (arduinoSensor)
2. Update map (mapping)
3. Get instructions based on map
4. Send out commands (arduinoMovement, arduinoPump)
"""
running = True
Accel = []
Echo = []
#individual sensors and their directions
FRONT1 = None
BACK1 = None
RIGHT1 = None
LEFT1 = None

Bump = "CLEAR"
Button = 0

while running:
    try:
        """
        Sensor values include:
        1. Accel [Angle_x, Angle_Y, Angle_Z]
        2. Echo [Sensor1, 2, ... etc]
        3. Bump [CLEAR/BUMP]
        4. Optical (but this is separate for now)
        """
        

        while arduinoSensor.in_waiting > 0:
            sensor_vals = arduinoSensor.readline().decode()
            sensor_vals = sensor_vals[:-1]
            sensor_vals = sensor_vals.split()
            if sensor_vals[0] == "ACCEL":
                Accel = sensor_vals[1:]
            elif sensor_vals[0] == "ECHO":
                Echo = sensor_vals[1:]
                #Assigning each reading to individual variable to make life easier
                FRONT1 = Echo[0]
                RIGHT1 = Echo[1]
                BACK1 = Echo[2]
                LEFT1 = Echo[3]
            elif sensor_vals[0] == "BUMP":
                Bump = "BUMP"
            elif sensor_vals[0] == "CLEAR":
                Bump = "CLEAR"
            elif sensor_vals[0] == "B1":
                if Button == 0:
                    Button = 1
                else:
                    Button = 0
        
        if Button == 1: #command to be issued
            cmd=input("Enter command: ")
            # cmd+=" "
            arduinoMove.write(cmd.encode())
            Button = 0


    except KeyboardInterrupt:
        print("\nclosing file")
        arduinoSensor.close()
        arduinoMove.close()
        running = False
