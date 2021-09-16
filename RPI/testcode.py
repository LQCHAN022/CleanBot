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
                        print("Something to be printed")
                        try: 
                            answer = arduino1.readline().decode()
                            answer = answer[:-1] #remove the newline behind
                            answer = answer.split()
                            print(answer)
                            # print(port)
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
                            else:
                                print("Found this instead:", answer[0])
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


valid = True
while valid:
    choice = int(input("What do test: \n \
    1. Sensor \n \
    2. Movement \n \
    3. Movement and Delta/Step test \n \
    4. Echo calibration \n\
    5. Clean testing \n    "))
    if choice == 1:
        """
                Updates the following attributes:
                1. self.Echo
                2. self.EchoHist
                3. self.Accel
                4. self.Bump
                5. self.B1
                6. self.B2
                7. self.(Optical stuff, not yet)
                """
        # robot.read("SENSOR")
        robot.scan()
        print("Echo:", robot.Echo)
        print("Echo Hist:", robot.EchoHist)
        print("Accel:", robot.Accel)
        print("Bump:", robot.Bump)
        print("B1:", robot.B1)
        print("B2:", robot.B2)
        for row in robot.Nmap.current:
            print(row[10:41])
        print("Nmap:", robot.Nmap.current)
        print("Nmap Echo", robot.Nmap.checksurr())
    elif choice == 2:
        cmd = input("Input dir<space>dist").split()
        cmd = [int(i) for i in cmd]
        robot.move(*cmd) #code does not pause here
        for _ in range(30):
            time.sleep(0.1)
            robot.read("MOVE")
            print("Dir:", robot.dir)
            print("State:", robot.state)
            print("Delta:", robot.Delta, "\n")
            # print("Step Count:", robot.step_count, "\n")
            # time.sleep(0.1)
    elif choice == 3:
        for _ in range(3):
            robot.move(0, -1)
            while(robot.state != "STOP"):
                robot.scan()
                if robot.Delta[0] >= 1:
                    robot.stop()
            robot.move(180, -1)
            while(robot.state != "STOP"):
                robot.scan()
                if robot.Delta[0] <= -1:
                    robot.stop()
    elif choice == 4:
        loop = int(input("How many times to loop"))
        for _ in range(loop):
            robot.scan()
            print("Echo Hist", robot.EchoHist)
            # print("Raw echo", robot.Echo)
            # print("Nmap Echo", robot.Nmap.checksurr())
            time.sleep(0.2)

    elif choice == 5:
        valid = True
        while valid:
            loop = int(input("1. on, 2. off, 3. exit"))
            if loop == 1:
                robot.cleanon()
            elif loop == 2:
                robot.cleanoff()
            else:
                valid = False



    # elif choice == 4:
    #     for _ in range(3):
    #         robot.move(0, -1)
    #         while(robot.state != "STOP"):
    #             robot.scan()
    #             if robot.Echo
