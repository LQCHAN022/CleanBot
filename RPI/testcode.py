"""
This code is to test the implementation of the various functions and classes
"""

import serial,time
from mapping import Map
from serial.serialutil import SerialException
from Robot import Robot
import numpy as np
import keyboard

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
on = True

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

np.set_printoptions(threshold=np.inf)
valid = True
while valid:
    choice = int(input("What do test: \n \
    1. Sensor \n \
    2. Movement \n \
    3. Movement and Delta/Step test \n \
    4. Echo calibration \n \
    5. Clean testing \n \
    6. Manual Control \n \
    7. Auto demo \n \
    8. Full Auto Demo \n \
    9. On/Off \n \
    0. Quit"))

    if choice == 0:
        valid = False
    
    elif choice == 1:
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
        for row in robot.Nmap.current:
            print(row[15:-34])
        print("Size of map now is row/col:", len(robot.Nmap.current), ",", len(robot.Nmap.current[0]))
        print("Echo:", robot.Echo)
        print("Echo Hist:", robot.EchoHist)
        print("Accel:", robot.Accel)
        print("Bump:", robot.Bump)
        print("B1:", robot.B1)
        print("B2:", robot.B2)
        print("Pos:", robot.Nmap.pos)
        # print("Nmap:\n", robot.Nmap.current)
        print("Nmap Echo", robot.Nmap.checksurr())
        # robot.Nmap.showcurrent(1)
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
        robot.scan()
        for _ in range(10):
            startpos = robot.Delta_raw[0]
            robot.move(0, -1)
            while(robot.state != "STOP"):
                robot.scan()
                print(robot.Delta)
                # print(robot.Delta_raw)
                if robot.Delta[0] <= -1:
                    # print(robot.Delta)
                    robot.stop()

            startpos = robot.Delta_raw[0]
            robot.move(180, -1)
            while(robot.state != "STOP"):
                robot.scan()
                print(robot.Delta)
                # print(robot.Delta_raw)
                if robot.Delta[0] >= 1:
                    # print(robot.Delta)
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
        validc = True
        while validc:
            loop = int(input("1. on, 2. off, 3. exit"))
            if loop == 1:
                robot.cleanon()
            elif loop == 2:
                robot.cleanoff()
            else:
                validc = False
    
    elif choice == 6:
        cleancheck = False
        validc = True
        while validc:
            robot.scan() #to clear stuff?
            ###   FRONT   ###
            if(keyboard.is_pressed("w")):
                print("w")
                robot.scan()
                if(robot.Nmap.checksurr().get("FRONT", 10)<5): #use dict
                    print("Warning")
                    robot.stop()
                    continue
                if(robot.Bump == "BUMP"):
                    print("BUMP!")
                    robot.stop()
                    continue
                robot.move(0, -1)
                # time.sleep(0.1)
                while(keyboard.is_pressed("w")):
                    robot.scan()
                    if(robot.Nmap.checksurr().get("FRONT", 10)<5): #use dict
                        print("Warning")
                        robot.stop()
                        print("Delta is {}, {}".format(robot.Delta[0], robot.Delta[1]))
                        break
                    if(robot.Bump == "BUMP"):
                        print("BUMP!")
                        robot.scan()
                        print("Delta is {}, {}".format(robot.Delta[0], robot.Delta[1]))
                        robot.stop()
                        break
                else:
                    print("w released")
                    robot.scan()
                    print("Delta is {}, {}".format(robot.Delta[0], robot.Delta[1]))
                    robot.stop()

            ###   BACK   ###
            elif(keyboard.is_pressed("s")):
                print("s")
                robot.move(180, -1)
                # time.sleep(0.1)
                while(keyboard.is_pressed("s")):
                    pass
                else:
                    print("s released")
                    robot.scan()
                    print("Delta is {}, {}".format(robot.Delta[0], robot.Delta[1]))
                    robot.stop()

            ###   CCW Cont   ###
            elif(keyboard.is_pressed("a")):
                print("a")
                robot.scan()
                if(robot.Nmap.checksurr().get("RIGHT", 10)<4 or robot.Nmap.checksurr().get("LEFT", 10)<4): #use dict
                    print("Warning")
                    robot.stop()
                    continue
                if(robot.Bump == "BUMP"):
                    print("BUMP!")
                    robot.stop()
                    continue
                robot.move(270, -1)
                # time.sleep(0.1)
                while(keyboard.is_pressed("a")):
                    robot.scan()
                    if(robot.Nmap.checksurr().get("RIGHT", 10)<4 or robot.Nmap.checksurr().get("LEFT", 10)<4): #use dict
                        print("Warning")
                        robot.stop()
                        print("Delta is {}, {}".format(robot.Delta[0], robot.Delta[1]))
                        break
                    if(robot.Bump == "BUMP"):
                        print("BUMP!")
                        print("Delta is {}, {}".format(robot.Delta[0], robot.Delta[1]))
                        robot.stop()
                        break
                else:
                    print("a released")
                    robot.stop()

            
            ###   CW Cont   ###
            elif(keyboard.is_pressed("d")):
                print("d")
                robot.scan()
                if(robot.Nmap.checksurr().get("RIGHT", 10)<4 or robot.Nmap.checksurr().get("LEFT", 10)<4): #use dict
                    print("Warning")
                    robot.stop()
                    continue
                if(robot.Bump == "BUMP"):
                    print("BUMP!")
                    robot.stop()
                    continue
                robot.move(90, -1)
                # time.sleep(0.1)
                while(keyboard.is_pressed("d")):
                    robot.scan()
                    if(robot.Nmap.checksurr().get("RIGHT", 10)<4 or robot.Nmap.checksurr().get("LEFT", 10)<4): #use dict
                        print("Warning")
                        robot.stop()
                        print("Delta is {}, {}".format(robot.Delta[0], robot.Delta[1]))
                        break
                    if(robot.Bump == "BUMP"):
                        print("BUMP!")
                        robot.scan()
                        print("Delta is {}, {}".format(robot.Delta[0], robot.Delta[1]))
                        robot.stop()
                        break
                else:
                    print("d released")
                    robot.stop()

            ###   CCW 270   ###
            elif(keyboard.is_pressed("q")):
                print("q")
                robot.move(270)
                while(keyboard.is_pressed("q")):
                    pass
                else:
                    print("q released")
                    robot.stop()

            ###   CW 90   ###
            elif(keyboard.is_pressed("e")):
                print("e")
                robot.move(90)
                while(keyboard.is_pressed("e")):
                    pass
                else:
                    print("e released")
                    robot.stop()

            elif(keyboard.is_pressed("c")):
                print("c")
                if(cleancheck):
                    robot.cleanoff()
                    cleancheck = False
                else:
                    robot.cleanon()
                    cleancheck = True
                while(keyboard.is_pressed("c")):
                    pass

            elif(keyboard.is_pressed("i")):
                print("i")
                robot.scan()
                print("Gyro: {}".format(robot.Accel))
                print("Surrounding check:", robot.Nmap.checksurr())
                print("Optical Coordinates:", robot.Delta_raw[0], robot.Delta_raw[1])
                print("Coordinates:", robot.Delta[0], robot.Delta[1])
                while(keyboard.is_pressed("i")):
                    pass
                else:
                    pass
                    
            elif(keyboard.is_pressed("x")):
                print("x")
                robot.stop()
                while(keyboard.is_pressed("x")):
                    pass
                else:
                    pass
            
            elif(keyboard.is_pressed("r")):
                robot.stop()
                validc = False

    elif choice == 7:
        state = "FRONT"
        robot.scan() #to clear stuff?

        ###   FRONT till stop  ###
        robot.move(0, -1)
        time.sleep(0.1)
        robot.cleanon()
        robot.scan()
        while(robot.Nmap.checksurr().get("FRONT", 10)>1): #use dict
            robot.scan()
            if robot.state == "STOP":
                break
        robot.stopall()
        time.sleep(0.1)

        ### BACK a bit  ###     
        robot.move(180, 5740) #move back 20cm
        while(robot.state != "STOP"):
            robot.scan()
            pass
        robot.stopall()

        ### CW 90 ###
        robot.move(90)
        robot.stop()
        time.sleep(0.1)

        ### FRONT a bit ###
        robot.move(0, 5740)
        time.sleep(0.1)
        robot.cleanon()
        while(robot.state != "STOP"):
            robot.scan()
            if(robot.Nmap.checksurr().get("FRONT", 10)<4): #use dict
                robot.stopall()
            if robot.state == "STOP":
                break
            pass
        robot.stopall()
        time.sleep(0.1)

        robot.scan()
        robot.move(90)
        robot.stop()
        time.sleep(0.1)
        
        robot.move(0, -1)
        time.sleep(0.1)
        robot.cleanon()
        robot.scan()
        while(robot.Nmap.checksurr().get("FRONT", 10)>1): #use dict
            robot.scan()
            if robot.state == "STOP":
                break
        robot.stopall()
        time.sleep(0.1)
    
    elif choice == 8:
        state = "FRONT"
        robot.scan() #to clear stuff?
        running = True
        lastShort = 0
        while running:
        
            robot.scan() #to clear stuff?

            ###   FRONT till stop  ###
            robot.move(0, -1)
            time.sleep(0.1)
            robot.cleanon()
            robot.scan()
            while(robot.Nmap.checksurr().get("FRONT", 10)>1): #use dict
                robot.scan()
                if robot.state == "STOP":
                    print("Obstacle detected")
                    break
            robot.stopall()
            time.sleep(0.1)

            ### BACK a bit  ###     
            robot.move(180, 5740) #move back 20cm
            while(robot.state != "STOP"):
                robot.scan()
                pass
            robot.stopall()

            ### CW 90 ###
            robot.move(90)
            robot.stop()
            time.sleep(0.1)

            ### FRONT a bit ###
            robot.move(0, 8610)
            time.sleep(0.1)
            robot.cleanon()
            while(robot.state != "STOP"):
                robot.scan()
                if(robot.Nmap.checksurr().get("FRONT", 10)<4): #stop with turning room
                    robot.stopall()
                    print("Obstacle detected")
                    if lastShort == 1:
                        robot.stopall()
                        running = False
                    lastShort = 1
                    break
                elif robot.Bump == "BUMP": #stop by collision
                    print("Obstacle detected")
                    robot.move(180, 5740) #move back 20cm to give turning space
                    # while(robot.state == "STOP"):
                    #     robot.scan()
                    robot.stopall()
                    if lastShort == 1:
                        robot.stopall()
                        running = False
                    lastShort = 1
                    break
                else:
                    lastShort = 0
            robot.stopall()
            time.sleep(0.1)

            if running == False:
                break
            ### CW 90 ###
            robot.scan()
            robot.move(90)
            robot.stop()
            time.sleep(0.1)
            
           ###   FRONT till stop  ###
            robot.move(0, -1)
            time.sleep(0.1)
            robot.cleanon()
            robot.scan()
            while(robot.Nmap.checksurr().get("FRONT", 10)>1): #use dict
                robot.scan()
                if robot.state == "STOP":
                    print("Obstacle detected")
                    break
            robot.stopall()
            time.sleep(0.1)

            ### BACK a bit  ###     
            robot.move(180, 5740) #move back 20cm
            while(robot.state != "STOP"):
                robot.scan()
                pass
            robot.stopall()

            ### CCW 270 ###
            robot.move(270)
            robot.stop()
            time.sleep(0.1)

            ### FRONT a bit ###
            robot.move(0, 8610)
            time.sleep(0.1)
            robot.cleanon()
            while(robot.state != "STOP"):
                robot.scan()
                if(robot.Nmap.checksurr().get("FRONT", 10)<4): #stop with turning room
                    robot.stopall()
                    print("Obstacle detected")
                    if lastShort == 1:
                        robot.stopall()
                        running = False
                    lastShort = 1
                    break
                elif robot.Bump == "BUMP": #stop by collision
                    print("Obstacle detected")
                    robot.move(180, 5740) #move back 20cm to give turning space
                    # while(robot.state != "STOP"):
                    #     robot.scan()
                    robot.stopall()
                    if lastShort == 1:
                        robot.stopall()
                        running = False
                    lastShort = 1
                    break
                else:
                    lastShort = 0
            robot.stopall()
            time.sleep(0.1)

            if running == False:
                break
            ### CW 90 ###
            robot.scan()
            robot.move(270)
            robot.stop()
            time.sleep(0.1)
            if robot.B2:
                running = False
        print("End of Cleaning")
        
    elif choice == 9:
        if(on):
            robot.off()
            print("Robot now off")
            on = False
        else:
            robot.on()
            print("Robot now on")
            on = True
