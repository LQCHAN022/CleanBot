class Robot():
    def __innit__(self, arduinoSensor, arduinoMove, arduinoPump, Nmap):
        self.state = None #what is the robot doing now
        self.ASense = arduinoSensor
        self.AMove = arduinoMove
        self.APump = arduinoPump
        self.Nmap = Nmap
        self.Echo = {"FRONT": None, "RIGHT": None, "LEFT": None} #should have a few conseq readings, set as 3 for now
        self.Accel = {}
        self.Bump = []
        self.Delta = []
        self.B1 = 0
        self.B2 = 0

    def move(self, dir, dist):
        """
        This method aims to move the robot
        """
        if dir == 0:
            self.AMove.write("FRONT {}".format(dist).encode())
        elif dir == 90:
            self.AMove.write("E 20700".encode())
        elif dir == 270:
            self.AMove.write("Q 20700".encode())
        elif dir == 180:
            self.AMove.write("E 41400".encode())
        self.AMove("R".encode())
    
    def stop(self):
        """
        This method aims to stop the robot
        """
        self.AMove.write("S".encode())

    def cleanon(self, pwm, sps):
        """
        This method aims to start the cleaning process
        Activates roller and pump
        pwm: duty cycle of pump
        sps: steps per second of roller motor
        """
        self.APump.write("ON {}".format(pwm).encode())
        self.Amove.write("CLEAN {}".format(sps).encode())
    
    def cleanoff(self):
        """
        This method turns off all cleaning related devices
        """
        self.APump.write("OFF".encode())
        self.Amove.write("CLEAN 0".encode())

    def stopall(self):
        """
        This method aim to stop everything
        """
        self.stop()
        self.cleanoff()

    def read(self, arduino):
        """
        This method aims to read and clean the data from the arduino to make coding easier
        Parameter will be in the form read("SENSOR") for example
        """
        #Pretty everything comes from here
        if arduino == "SENSOR":
            while self.ASense.in_waiting > 0: #while there's stuff in the buffer to be read
                Sense_vals = arduino.readline().decode() #read the string
                Sense_vals = Sense_vals[:-1] #take away the \n at the back
                Sense_vals = Sense_vals.split() #split it into elements in a list, based on space " "
                #format for sensor vals: ["<TYPE>", "val1", "val2", ...]
                if Sense_vals[0] == "ECHO": #over here for now I'm treating the front as one whole so yeah
                    """
                    We need to get stable, and minimum value
                    Stable is defined as low fluctuation for 2 conseq senses
                    Stability check will be done in updating side 

                    FRONT: 1, 2, 3, 4
                    RIGHT: 5, 6
                    LEFT: 7, 8
                    """
                    try:
                        #won't really work for the first run, this is to pass previous run's to previous previous run
                        self.Echo["PFront"] = self.Echo["FRONT"]
                        self.Echo["PRight"] = self.Echo["RIGHT"]
                        self.Echo["PLeft"] = self.Echo["LEFT"]
                        
                        Front = [int(i) for i in Sense_vals[1:5]]
                        Right = [int(i) for i in Sense_vals[5:7]]
                        Left = [int(i) for i in Sense_vals[7:9]]

                        self.Echo["FRONT"] = min(Front)
                        self.Echo["RIGHT"] = min(Right)
                        self.Echo["LEFT"] = min(Left)
                    except:
                        pass

                elif Sense_vals[0] == "ACCEL":
                    self.Accel["X"] = Sense_vals[1]
                    self.Accel["Y"] = Sense_vals[2]
                    self.Accel["Z"] = Sense_vals[3]
                
                elif Sense_vals[0] == ""

        #MOVE is important cause we want to know when the motors have finished moving
        elif arduino == "MOVE":
            while self.AMove.in_waiting > 0: #while there's stuff in the buffer to be read
                Move_vals = arduino.readline().decode() #read the string
                Move_vals = Move_vals[:-1] #take away the \n at the back
                Move_vals = Move_vals.split() #split it into elements in a list, based on space " "
        
        #PUMP usually don't send anything over this is just here for fun
        elif arduino == "PUMP":
            while self.APump.in_waiting > 0: #while there's stuff in the buffer to be read
                Pump_vals = arduino.readline().decode() #read the string
                Pump_vals = Pump_vals[:-1] #take away the \n at the back
                Pump_vals = Pump_vals.split() #split it into elements in a list, based on space " "
    
    def scan(self, Nmap):
        """
        The method aims to scan the surroundings and update the map accordingly
        Also updates own position
        """
        while self.ASensor.in_waiting > 0:
            sensor_vals = self.ASensor.readline().decode()
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
