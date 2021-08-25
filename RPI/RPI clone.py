#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial,time
from mapping import Map
from serial.serialutil import SerialException
from Robot import Robot

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
"""
Task list:
1. Pathfinding
2. Configure optical
3. Convert the thing below to work with robot
4. Adjust speed of motors
5. Determine the power required
6. Set up the rest of the sensors

How it flows:
scan arduinoSensor to scan and process surrounding data
access attributes in logic and determine what to do
scan arduinoMove in case
move to move (but note that map does not update from this)
scan arduinoMove to get how much travelled or update orientation ALWAYS SCAN BEFORE AND AFTER MOVEMENT COMMAND
"""
robot = Robot(arduinoSensor, arduinoMove, arduinoPump)
Nmap = robot.Nmap
safelim = 4

Nmap.expandcheck()
# Nmap.showcurrent(1)
running = True

state = "NORTH" #current state //note that these state are for the logic and not for the robot action state
pstate = None #previous state

while robot.B2:
    robot.scan()

while running:
    robot.scan()

    while state == "NORTH" or state == "SOUTH":
        robot.scan()
        if Nmap.checksurr().get("FRONT", 10) >= safelim:
            if robot.state == "STOP":
                robot.move(0, -1) #move forward indefinitely
                robot.cleanon()
        else:
            robot.stopall() #staph
            pstate = state
            state = "OBSTACLE"

    while state == "OBSTACLE":
        robot.scan()
        if Nmap.checksurr().get("FRONT", 10) < safelim: #if front has something, redundant but just in case
            if pstate == "NORTH": 
                if Nmap.checksurr().get("RIGHT", 10) >= safelim: #if right is clear
                    robot.move(90) #command will stay here until movement is finished, which also makes it prone to accidents but eh
                    state = "EAST"
                else:
                    robot.scan()
                    while Nmap.checksurr().get("RIGHT", 10) < safelim and Nmap.checksurr().get("BACK", 10) >= safelim: #while right not clear and back clear
                        robot.scan()
                        if robot.state == "STOP":
                            robot.move(180, -1) #reverse
                    else:
                        if Nmap.checksurr().get("RIGHT", 10) >= safelim: #if right cleared alr
                            robot.move(90)
                            state = "EAST"
                        else: #if back hit limit alr
                            state = "RIGHT_WALL"

            elif pstate == "SOUTH":
                if Nmap.checksurr().get("LEFT", 10) >= safelim:
                    robot.move(270)
                    state = "EAST"
                else:
                    while Nmap.checksurr().get("LEFT", 10) < safelim and Nmap.checksurr().get("BACK", 10) >= safelim: #while left not clear and back clear
                        robot.scan()
                        if robot.state == "STOP":
                            robot.move(180, -1)
                    else:
                        if Nmap.checksurr().get("LEFT", 10) >= safelim: #if left cleared alr
                            robot.move(270)
                            state = "EAST"
                        else: #if back hit limit alr
                            state = "RIGHT_WALL"



        else: #go back to whatever
            state = pstate

    while state == "EAST": 
        robot.scan()
        if pstate == "NORTH":
            if Nmap.checksurr().get("RIGHT", 10) < safelim and Nmap.checksurr().get("FRONT", 10) < safelim: #if both RIGHT and FRONT blocked
                while Nmap.checksurr().get("RIGHT", 10) < safelim and Nmap.checksurr().get("BACK", 10) >= safelim: #while RIGHT not clear and BACK clear
                        robot.scan()
                        if robot.state == "STOP":
                            robot.move(180, -1)
                else:
                    if Nmap.checksurr().get("RIGHT", 10) >= safelim: #if RIGHT cleared alr
                        robot.move(270)
                        state = "SOUTH"
                    else: #if back hit limit alr
                        state = "RIGHT_WALL"
            elif Nmap.checksurr().get("RIGHT", 10) < safelim and Nmap.checksurr().get("FRONT", 10) >= safelim: #if only RIGHT blocked
                if robot.state == "STOP":
                    robot.move(0, -1)
            elif Nmap.checksurr().get("FRONT", 10) < safelim and Nmap.checksurr().get("RIGHT", 10) >= safelim: #if only FRONT blocked
                if robot.state == "STOP":
                    robot.move(180, -1)
            else: #both sides free
                robot.move(0, 4305)
                while robot.state != "STOP": #while moving just carry on
                    robot.scan()
                    if Nmap.checksurr().get("FRONT", 10) < safelim:
                        robot.stopall()
                pstate = state
                state = "SOUTH"
                robot.move(90)

        elif pstate == "SOUTH":
            if Nmap.checksurr().get("LEFT", 10) < safelim and Nmap.checksurr().get("FRONT", 10) < safelim: #if both LEFT and FRONT blocked
                while Nmap.checksurr().get("LEFT", 10) < safelim and Nmap.checksurr().get("BACK", 10) >= safelim: #while LEFT not clear and BACK clear
                        robot.scan()
                        if robot.state == "STOP":
                            robot.move(180,-1)
                else:
                    if Nmap.checksurr().get("LEFT", 10) >= safelim: #if LEFT cleared alr
                        robot.move(270)
                        state = "NORTH"
                    else: #if back hit limit alr
                        state = "RIGHT_WALL"
            elif Nmap.checksurr().get("LEFT", 10) < safelim and Nmap.checksurr().get("FRONT", 10) >= safelim: #if only LEFT blocked
                if robot.state == "STOP":
                    robot.move(0, -1)
                    robot.cleanon()
            elif Nmap.checksurr().get("FRONT", 10) < safelim and Nmap.checksurr().get("LEFT", 10) >= safelim: #if only FRONT blocked
                if robot.state == "STOP":
                    robot.move(180, -1)
            else: #both sides free
                robot.move(0, 4305)
                while robot.state != "STOP": #while moving just carry on
                    robot.scan()
                    if Nmap.checksurr().get("FRONT", 10) < safelim:
                        robot.stopall()
                pstate = state
                state = "NORTH"
                robot.move(270)
    
    if state == "RIGHT_WALL":
        print("That's it folks")
        running = False