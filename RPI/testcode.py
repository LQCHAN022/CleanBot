"""
This code is to test the implementation of the various functions and classes
"""

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
nports = 3 #number of ports/connections
missingArduino = True
connected = False

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
                            print(port)
                            if answer[0] == "SENSOR": #assigns the connected arduino to it's correct name
                                checkdone = True
                                arduinoSensor = arduino1
                                print("Sensor found")
                                
                            elif answer[0] == "MOVEMENT":
                                checkdone = True
                                arduinoMove = arduino1
                                print("Movement found")
                                
                            elif answer[0] == "PUMP":
                                checkdone = True
                                arduinoPump = arduino1
                                print("PUMP found")
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

robot = Robot(arduinoSensor, arduinoMove, arduinoPump)

robot.move(0, -1)
time.sleep(1)
robot.cleanon()
time.sleep(5)
robot.stopall()