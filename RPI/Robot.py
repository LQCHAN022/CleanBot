from mapping import Map
import math
import serial,time
from mapping import Map
from serial.serialutil import SerialException

class Robot():
    def __init__(self, arduinoSensor, arduinoMove, arduinoPump):
        #These three are responsible of tracking the robot state of motion 
        self.state = None #what is the robot doing now, eg. FRONT, BACK, RIGHT, LEFT, ETURN, QTURN, ...
        self.pstate = None #used to record previous state
        self.rotate = False #states if the rotation is done, no use as of now
        self.Delta = [0, 0] #will be in the row and col format, not x and y, this will be the coordinate of the robot in the most accurate sense, since that of Nmap only supports integer values
                            #Delta be true delta instead of compensated delta?(like in mapping since origin for that is fixed and moving)
                            #There has to be attribute in mapping to take care of the deformation called self.deform
        self.step_count = 0 #this stored that last value of the stepper steps

        #These are the different Arduinos
        self.ASense = arduinoSensor
        self.AMove = arduinoMove
        self.APump = arduinoPump
        
        #map initialisation will be done here
        self.Nmap = Map(30, [9, 15]) #[9, 15]
        self.Nmap.setpos(15, 15, "N")
        self.Nmap.sethome(15, 15, "N")
        self.Nmap.expandcheck()
        self.setdir("N")
        
        self.Echo = {"FRONT": None, "RIGHT": None, "LEFT": None} #the data in this is in cm, not grids
        self.EchoHist = {"FRONT": [], "RIGHT": [], "LEFT": []} #This is a dictionary with lists containing history of echo readings and whenever there are two consecutive readings it will pass to self.Echo

        self.Accel = {} 
        self.Bump = "CLEAR"
        
        self.B1 = False
        self.B2 = False

    def printattr(self):
        print("State:", self.state)
        print("Delta:", self.Delta)
        print("Rotate:", self.rotate)

    def newstate(self, newstate):
        """
        Updates the state but implemented in functions already
        Just a smaller function to reduce two lines of code into one
        """
        self.pstate = self.state
        self.state = newstate
    
    def move(self, dir, dist = 20700):
        """
        This method aims to move the robot
        Handles negative steps for rotation ie it will turn the other way
        Note that forward and backwards different than in mapping cause -1 with front will cause infinite running
        """
        # self.stop() #failsafe
        # if not self.B2:
        #     return
        time.sleep(0.1)
        print("Move passed with", dir, dist)
        if dir == 0:
            self.AMove.write("FRONT {}\n".format(dist).encode())
            self.newstate("FRONT")
        elif dir == 180:
            self.AMove.write("BACK {}\n".format(dist).encode())
            self.newstate("BACK")
        else: #allows to negatve angles so the speak
            if dist < 0:
                dir = 90 if dir == 270 else 270
                dist = -dist
            if dir == 90:
                cmd = "E " + str(dist) + "\n"
                self.AMove.write(cmd.encode())
                self.newstate("ETURN")
                # self.Accel["PZ"] = self.Accel["Z"]
            elif dir == 270:
                cmd = "Q " + str(dist) + "\n"
                self.AMove.write(cmd.encode())
                self.newstate("QTURN")
                # self.Accel["PZ"] = self.Accel["Z"]
        self.rotate = False
        time.sleep(0.1)
        self.AMove.write("R\n".encode())
        
        #set things to pause until rotation complete
        if dir == 90 or dir == 270:
            while not self.rotate:
                self.scan()
                print(self.Accel)
    
    def stop(self):
        """
        This method aims to stop the robot
        """
        self.AMove.write("S\n".encode())
        self.newstate("STOP")

    def cleanon(self, pwm = 255, sps = 1000):
        """
        This method aims to start the cleaning process
        Activates roller and pump
        pwm: duty cycle of pump
        sps: steps per second of roller motor
        """
        self.APump.write("ON {}\n".format(pwm).encode())
        self.AMove.write("CLEAN {}\n".format(sps).encode())
    
    def cleanoff(self):
        """
        This method turns off all cleaning related devices
        """
        self.APump.write("OFF\n".encode())
        self.AMove.write("CLEAN 0\n".encode())

    def stopall(self):
        """
        This method aim to stop everything
        """
        self.stop()
        time.sleep(0.5)
        self.cleanoff()

    def setdir(self, dir):
        """
        Updates both the self.dir in Robot and in the map
        Makes-my-life-easier function
        """
        self.dir = dir
        self.Nmap.dir = dir

    def read(self, arduino):
        """
        This method aims to read and clean the data from the arduino to make coding easier
        Parameter will be in the form read("SENSOR") for example
        Does not return anything, but instead updates the respective attributes
        """
        #Pretty everything comes from here
        if arduino == "SENSOR":
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
            while self.ASense.in_waiting > 0: #while there's stuff in the buffer to be read
                Sense_vals = self.ASense.readline().decode() #read the string
                Sense_vals = Sense_vals[:-1] #take away the \n at the back
                Sense_vals = Sense_vals.split() #split it into elements in a list, based on space " "
                #format for sensor vals: ["<TYPE>", "val1", "val2", ...]
                if Sense_vals[0] == "ECHO": #over here for now I'm treating the front as one whole so yeah
                    """
                    We need to get stable, and minimum value
                    Stable is defined as low fluctuation for 2 conseq senses
                    What it does it to compare it with the last reading then if it is within a certain range it is stable
                    Then among the stable ones it will return the one with the min value
                    
                    Which reading corresponds to which direction
                    FRONT: 1, 2, 3, 4
                    LEFT: 5, 6
                    RIGHT: 7, 8
                    """
                    
                    #This part separates the different values into their respective directions, maybe can be optimised if use list?
                    EchoReadings = {}
                    EchoReadings["FRONT"] = [int(i) for i in Sense_vals[1:5]] 
                    EchoReadings["LEFT"] = [int(i) for i in Sense_vals[5:7]] 
                    EchoReadings["RIGHT"] = [int(i) for i in Sense_vals[7:9]] 
                    # print(EchoReadings)
                    
                    for dir in ["FRONT", "RIGHT", "LEFT"]:
                        if len(self.EchoHist[dir]) == 0: #if there are no records of previous readings
                            # print("Initial")
                            self.EchoHist[dir] = EchoReadings[dir] #update the history with the current readings
                            self.Echo[dir] = min(EchoReadings[dir]) #update the attributes with the lowest of current value
                        else:
                            StableVals = []
                            for i in range(len(EchoReadings[dir])): #checking the each of the readings of each direction
                                if abs(EchoReadings[dir][i] - self.EchoHist[dir][i]) < 20: #if it varies from the previous by less than 20
                                    StableVals.append(EchoReadings[dir][i]) #list of stable values for this direction contains...
                                    # print(StableVals, dir)
                            if len(StableVals) != 0: #somehow or another bugged sometimes so yeah this is here in case
                                self.Echo[dir] = min(StableVals) #minimum of the stable values
                            self.EchoHist[dir] = EchoReadings[dir]

                            
                            
                elif Sense_vals[0] == "ACCEL":
                    """
                    Two important parts for this, as this is mainly used for turning it needs a before and after to compare
                    And it needs to read move complete too to know that it has been completed
                    We don't really need to monitor this constantly yet so yeah this is lowkey inefficient
                    """
                    self.Accel["X"] = Sense_vals[1]
                    self.Accel["Y"] = Sense_vals[2]
                    self.Accel["Z"] = Sense_vals[3]
                
                elif Sense_vals[0] == "BUMP" or Sense_vals[0] == "CLEAR":
                    self.Bump = Sense_vals[0]
                    

                elif Sense_vals[0] == "B1":
                    """
                    Basically toggles the Boolean value   
                    """
                    self.B1 = True if self.B1 == False else False
                
                elif Sense_vals[0] == "B2":
                    """
                    Basically toggles the Boolean value 
                    """
                    self.B2 = True if self.B2 == False else False

                elif Sense_vals[0] == "OPTICAL":
                    pass

        #MOVE is important cause we want to know when the motors have finished moving
        elif arduino == "MOVE":
            """
            Updates the following attributes:
            1. self.rotate
            2. self.Delta
            """
            while self.AMove.in_waiting > 0: #while there's stuff in the buffer to be read
                Move_vals = self.AMove.readline().decode() #read the string
                Move_vals = Move_vals[:-1] #take away the \n at the back
                Move_vals = Move_vals.split() #split it into elements in a list, based on space " "
                # print("Move read:", Move_vals)
                if Move_vals[0] == "MOVE_COMPLETE":
                    #this part takes note of the rotation such that it updates the direction when the rotation is finished
                    #doesn't do anything when movement front and reverse stops
                    self.newstate("STOP")
                    if self.dir == "N":
                        if self.pstate == "ETURN":
                            self.setdir("E")
                        elif self.pstate == "QTURN":
                            self.setdir("W")
                    elif self.dir == "E":
                        if self.pstate == "ETURN":
                            self.setdir("S")
                        elif self.pstate == "QTURN":
                            self.setdir("N")
                    elif self.dir == "S":
                        if self.pstate == "ETURN":
                            self.setdir("W")
                        elif self.pstate == "QTURN":
                            self.setdir("E")
                    elif self.dir == "W":
                        if self.pstate == "ETURN":
                            self.setdir("N")
                        elif self.pstate == "QTURN":
                            self.setdir("S")
                    #Need to check if previous turn was 90 degrees
                    #The sensor seems sus so I'm gonna leave it first
                    if self.pstate == "QTURN" or self.pstate == "ETURN":
                        self.rotate = True #remember to set it at false when executing the initial turn
                
                elif Move_vals[0] == "STEPS":
                    #grids is a temporary local variable cause I don't feel like typing the entire thing
                    #one grid is one "pixel" of 5cm on the map
                    # print("Current Steps:", Move_vals[1])
                    # print("Previous Steps:", self.step_count)
                    grids = abs((int(Move_vals[1]) - self.step_count)/1435)
                    # print("Grids:", grids)
                    self.step_count = int(Move_vals[1])
                    if self.state == "FRONT" or self.pstate == "FRONT": #if current action update or stopped update
                        if self.dir == "N":
                            self.Delta[0] += grids
                        elif self.dir == "S":
                            self.Delta[0] -= grids
                        elif self.dir == "E":
                            self.Delta[1] += grids
                        elif self.dir == "W":
                            self.Delta[1] -= grids

                    elif self.state == "BACK" or self.pstate == "BACK":
                        if self.dir == "N":
                            self.Delta[0] -= grids
                        elif self.dir == "S":
                            self.Delta[0] += grids
                        elif self.dir == "E":
                            self.Delta[1] -= grids
                        elif self.dir == "W":
                            self.Delta[1] += grids
                    
                    #redundant but hey future support
                    elif self.state == "LEFT":
                        if self.dir == "N":
                            self.Delta[1] -= grids
                        elif self.dir == "S":
                            self.Delta[1] += grids
                        elif self.dir == "E":
                            self.Delta[0] -= grids
                        elif self.dir == "W":
                            self.Delta[0] += grids

                    elif self.state == "RIGHT":
                        if self.dir == "N":
                            self.Delta[1] += grids
                        elif self.dir == "S":
                            self.Delta[1] -= grids
                        elif self.dir == "E":
                            self.Delta[0] += grids
                        elif self.dir == "W":
                            self.Delta[0] -= grids
                    

        
        #PUMP usually don't send anything over this is just here for fun
        elif arduino == "PUMP":
            while self.APump.in_waiting > 0: #while there's stuff in the buffer to be read
                Pump_vals = self.APump.readline().decode() #read the string
                Pump_vals = Pump_vals[:-1] #take away the \n at the back
                Pump_vals = Pump_vals.split() #split it into elements in a list, based on space " "
    
    def scan(self):
        """
        The method aims to scan the surroundings using self.read() and update the map accordingly
        Two things to update
        1. Obstacles/Clear (Echo and Bump for now)
        2. Own position (only raw feed back from motor and instructions ie. delta, assuming that rotation is right)
            Might have to rely on optical more than MPU
        """
        self.read("SENSOR")
        self.read("MOVE")
        # print("B2:", self.B2)
        # if self.B2 == False:
        #     self.stopall()

        #to get the theoretical location we need to ascertain how many steps were moved
        
        #This one updates the obstacles and free spaces
        #This one updates the position according to any new movements
        self.Nmap.DeltaPos([int(i) for i in self.Delta], self.dir)
        
        self.Nmap.expandcheck()
        for dir in ["FRONT", "LEFT", "RIGHT"]:
            self.Nmap.placeclr_rel(dir, self.Echo[dir]//5) #this must go first
            if self.Echo[dir] < 80: #this is in cm
                self.Nmap.placeob_rel(dir, math.floor(self.Echo[dir]/5)) #so anything obstacle override blank rather than vice versa
                print("placed obs", dir, "grids:", math.floor(self.Echo[dir]/5))
        if self.Bump == "BUMP":
            #if this happens during rotation it's gg
            self.Nmap.placeob_rel("FRONT", 1)
            self.stop()
            self.rotate = True

        

