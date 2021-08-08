import pathfind
import matplotlib.pyplot as plt
import time
import numpy as np

class Map:
    """
    Both x and y sizes must be odd numbered
    Note that coordinate system is row and col not x and y
    
    0: Indicates Obstacle
    10: Indicates Position of robot
    11: Indicates Front of robot
    1: Indicates Clear
    2: Indicates Cleaned
    3: Indicates Unknown


    """
    def __init__(self, s, size): #note size is rol col aka y/x
        data = np.full([s,s], 3) #generates a s times s map full of 3s (3 == unknown)
        data = np.array(data) #redundant code from before might remove in the future cause data is already array
        data = data.astype(int) #changes type from float to int, might be redundant
        self.current = data #attribute of type array that holds all the map information
        self.image = 0 #image data type from imshow(), used to update 
        self.size = size #list with y and x sizes of robot respectively, with x is how broad while y is how long
        self.home = None #list coordinates of where home is
        self.pos = None #list coordinates of current position
        self.dir = None #direction the robot is currently facing
        self.rows = s #how tall is the map in the North South direction
        self.cols = s   #how wide is the map in the East West direction                  < width >   
        self.safelim = 11 #how much space(-1) to raise that an obstacle is in front      # # # # #   ▲
        self.length = size[0] #note that the length is shorter than the width            # # # # # length
        self.width = size[1]                                                             # # # # #   ▼

    def setpos(self, y, x, dir): #sets position by coordinates and direction
        self.current[self.current == 10] = 2 #sets all 1 and 9 to 0 to clear old position
        self.current[self.current == 11] = 2
        self.current[y, x] == 10 #sets pivot. actually redundant code but take note of rol/col vs x/y
        self.dir = dir
        if dir == "N" or dir == "S":
            try:
                x_range = self.width//2 #how many pixels out from the middle
                y_range = self.length//2
                for i in range(x-x_range, x+x_range+1): #fill position with appropriately sized box to represent robot
                    for j in range(y-y_range, y+y_range+1):
                        self.current[j, i] = 10 #not j and i are for y and x respectively
                        # print(self.current)
            except IndexError:
                print("Position set too close to walls of map.")
            if dir == "N": #these are for indicating which side the robot is facing
                self.current[y-y_range, x] = 11
            elif dir == "S":
                self.current[y+y_range, x] = 11
        elif dir == "E" or dir == "W":
            try:
                x_range = self.width//2 
                y_range = self.length//2
                for i in range(x-y_range, x+y_range+1): #flipped x_range and y_range with flipped orientation
                    for j in range(y-x_range, y+x_range+1):
                        self.current[j, i] = 10
            except IndexError:
                print("Position set too close to walls of map.")
            if dir == "E":
                self.current[y, x+y_range] = 11 #the reason why y is used is cause orientation is flipped, 
            elif dir == "W":                    #in the x of picture is "y" of robot
                self.current[y, x-y_range] = 11
    
        self.pos = [y, x]

    def updatepos(self): 
        """
        #pushes the changes to attributes to the map/self.current
        
        """
        self.setpos(*self.pos, self.dir)


    def placeob(self, nw, se): 
        """
        places a obstacle with corners (north-west/south-east) at set position

        """
        #note that sw and ne are lists containing coordinates
        for row in range(nw[0], se[0]+1):
            for col in range(nw[1], se[1]+1):
                self.current[row, col] = 2

    def placeob_rel(self, dir, dist):
        """
        Places an obstacle at a set direction (prefixed length or ...?) at a set distance from the robot
        Obstacle will be one layer thick
        """
        pass
    

    def getcurrentpos(self): #returns the x, y, dir of current position
        return self.pos
    
    def sethome(self, y, x, dir):
        self.home = [y, x, dir]
        

    def gethome(self): #returns the coordinates of the home position
        return self.home
        

    def expand(self, size, dir): 
        """
        expands map in certain direction by size

        things to update (coordinate attributes):
        self.pos
        self.home
        self.dir remember

        self.current
        self.image, etc.
        """
        #Expanding the current map
        if dir == "E":
            self.current = np.append(self.current, np.full([self.rows, size], 3), axis = 1)
            self.cols += size
            #self.pos no need to update
        elif dir == "W":
            self.current = np.c_[np.full([self.rows, size], 3), self.current]
            self.cols += size
            self.pos[1] += size
            self.home[1] += size
        elif dir == "N":
            self.current = np.insert(self.current, 0, np.full([size, self.cols], 3), axis = 0)
            self.rows += size
            self.pos[0] += size
            self.home[0] += size
        elif dir == "S":
            self.current = np.append(self.current, np.full([size, self.cols], 3), axis = 0)
            self.rows += size
            #self.pos no need to update
        self.updatepos()
    
    def expandcheck(self):
        """
        Purpose of this is to check if there's a minimum clearance between the robot and the edge of the map, if there isn't expand
        """
        
        edge_y = self.rows - self.pos[0] - self.length #distance between robot and South edge
        edge_x = self.cols - self.pos[1] - self.width #distance between robot and East edge
        if edge_y < 20:
            self.expand(20, "S")
        if edge_x < 20:
            self.expand(20, "E")
        if self.pos[0] < 20:
            self.expand(20, "N")
        if self.pos[1] < 20:
            self.expand(20, "W")

    def showcurrent(self, t):
        """
        Displays and updates the current image of the map, somehow cannot work in RPI mode but eh
        Use t == -1 to just show one once, code after won't run though, somehow, I think
        """
        if self.image == 0:
            # print("First image")
            self.fig, self.ax = plt.subplots(1, 1)
            self.image = plt.imshow(self.current)
            # plt.show()
        else:
            # print("test")
            self.image.set_data(self.current)
            self.fig.canvas.draw_idle()
        # print(self.current)
        if t >= 0:
            plt.pause(t)
        else:
            plt.show()  


    def move(self, dir_rel, dist): #sets position by relative
        """
        Purpose is to move the robot in a set direction (0, 90, 180, 270) in a set distance. Note that robot can only move linearly when dir = 0 ie. robot not rotating
        """
        # self.pos[0] += col_move
        # self.pos[1] += row_move
        if self.dir == "N":
            if dir_rel == 0:
                self.dir = "N"
                self.pos[0] -= dist
            elif dir_rel == 90:
                self.dir = "E"
            elif dir_rel == 190:
                self.dir = "s"
            elif dir_rel == 270:
                self.dir = "W"
        elif self.dir == "E":
            if dir_rel == 0:
                self.dir = "E"
                self.pos[1] += dist
            elif dir_rel == 90:
                self.dir = "S"
            elif dir_rel == 190:
                self.dir = "W"
            elif dir_rel == 270:
                self.dir = "N"
        elif self.dir == "S":
            if dir_rel == 0:
                self.dir = "S"
                self.pos[0] += dist
            elif dir_rel == 90:
                self.dir = "W"
            elif dir_rel == 190:
                self.dir = "N"
            elif dir_rel == 270:
                self.dir = "E"
        elif self.dir == "W":
            if dir_rel == 0:
                self.dir = "W"
                self.pos[1] -= dist
            elif dir_rel == 90:
                self.dir = "N"
            elif dir_rel == 190:
                self.dir = "E"
            elif dir_rel == 270:
                self.dir = "S"

        self.updatepos() #pushes changes to map aka self.current
        self.expandcheck()
        self.showcurrent(0.1)

    def checksurr(self):

        """
        This function is to provide a list of directions and distancesrelative to the robot where obstacles are detected, based on self.safelim
        take note that the "length"/size[0] of the robot is shorter than it's width due to its shape
        the lowest dist is 1 when difference between coordinates of obstacle and edge of robot is 1
        
        
        """

        obsdir = [] #obstacle directions
        #North/South orientated check
        if self.dir == "N" or self.dir == "S": #this is needed cause different orientation will have different widths
            #checks in the North and South directions
            for col in range(self.pos[1]-self.width//2, self.pos[1] + self.width//2 + 1): #i refers to the index of the width to check self.width refers to the width of the robot, pos[1] refers to the col/x coord of the robot
                #checking north
                for row in range(self.pos[0] - self.length//2 - self.safelim, self.pos[0] - self.length//2): #the space to check North
                    if self.current[row, col] == 0: #North check
                        if self.dir == "N":
                            obsdir.append(["FRONT", self.pos[0] - self.length//2 - row]) #self.pos[1] - self.length//2 - col is the distance from the north edge to the assessed block
                        elif self.dir == "S":
                            obsdir.append(["BACK", self.pos[0] - self.length//2 - row])
                    
                    #This is mainly for wall hug, checking if cleaned
                    elif self.current[row, col] == 2: #North check
                            if self.dir == "N":
                                obsdir.append(["FRONTC", self.pos[0] - self.length//2 - row]) #self.pos[1] - self.length//2 - col is the distance from the north edge to the assessed block
                            elif self.dir == "S":
                                obsdir.append(["BACKC", self.pos[0] - self.length//2 - row])
                #     print("NORTH", row, col)
                #     self.current[row, col] = 20
                # print()
                   
                #checking south
                for row in range(self.pos[0] + self.length//2 + 1, self.pos[0] + self.length//2 + self.safelim + 1): #the space to check South
                    if self.current[row, col] == 0: #South check
                        if self.dir == "N": 
                            obsdir.append(["BACK", row - self.pos[0] - self.length//2]) #col - self.pos[1] - self.length//2] is the distance from the south edge to the assessed block
                        elif self.dir == "S": 
                            obsdir.append(["FRONT", row - self.pos[0] - self.length//2])
                    
                    elif self.current[row, col] == 2: #South check
                        if self.dir == "N": 
                            obsdir.append(["BACKC", row - self.pos[0] - self.length//2]) #col - self.pos[1] - self.length//2] is the distance from the south edge to the assessed block
                        elif self.dir == "S": 
                            obsdir.append(["FRONTC", row - self.pos[0] - self.length//2])
                #     print("SOUTH", row, col)
                #     self.current[row, col] = 20
                # print()

            #checks in the East and West directions
            for row in range(self.pos[0] - self.length//2, self.pos[0] + self.length//2 + 1): #row refers to the index of the width to check while self.length refers to the length of the robot
                #checking west
                for col in range(self.pos[1] - self.width//2 - self.safelim, self.pos[1] -  self.width//2): 
                    if self.current[row, col] == 0:
                        if self.dir == "N":
                            obsdir.append(["LEFT", self.pos[1] - self.width//2 - col]) #self.pos[1] - self.width//2 - col refers to the dist between the west edge and the robot
                        elif self.dir == "S":
                            obsdir.append(["RIGHT", self.pos[1] - self.width//2 - col])
                    
                    elif self.current[row, col] == 2:
                        if self.dir == "N":
                            obsdir.append(["LEFTC", self.pos[1] - self.width//2 - col]) #self.pos[1] - self.width//2 - col refers to the dist between the west edge and the robot
                        elif self.dir == "S":
                            obsdir.append(["RIGHTC", self.pos[1] - self.width//2 - col])
                    # print("WEST", row, col)
                #     self.current[row, col] = 20
                # print()

                #checking east
                for col in range(self.pos[1] + self.width//2 + 1, self.pos[1] + self.width//2 + self.safelim + 1):
                    if self.current[row, col] == 0:
                        if self.dir == "N":
                            obsdir.append(["RIGHT", col - self.pos[1] - self.width//2])
                        elif self.dir == "S":
                            obsdir.append(["LEFT", col - self.pos[1] - self.width//2])
                    
                    elif self.current[row, col] == 2:
                        if self.dir == "N":
                            obsdir.append(["RIGHTC", col - self.pos[1] - self.width//2])
                        elif self.dir == "S":
                            obsdir.append(["LEFTC", col - self.pos[1] - self.width//2])
                    # print("EAST", row, col)
                #     self.current[row, col] = 20
                # print()
                        

        #East/West orientated check
        if self.dir == "E" or self.dir == "W": #this is needed cause different orientation will have different widths
            #checks in the North and South directions
            for col in range(self.pos[1]-self.length//2, self.pos[1] + self.length//2 + 1): #i refers to the index of the width to check self.width refers to the width of the robot, pos[1] refers to the col/x coord of the robot
                #checking north
                for row in range(self.pos[0] - self.width//2 - self.safelim, self.pos[0] - self.width//2): #the space to check North
                    if self.current[row, col] == 0: #North check
                        if self.dir == "E":
                            obsdir.append(["LEFT", self.pos[0] - self.width//2 - row])
                        elif self.dir == "W": 
                            obsdir.append(["RIGHT", self.pos[0] - self.width//2 - row])
                    
                    elif self.current[row, col] == 2: #North check
                        if self.dir == "E":
                            obsdir.append(["LEFTC", self.pos[0] - self.width//2 - row])
                        elif self.dir == "W": 
                            obsdir.append(["RIGHTC", self.pos[0] - self.width//2 - row])
                #     print("NORTH", row, col)
                #     self.current[row, col] = 20
                # print()
                   
                #checking south
                for row in range(self.pos[0] + self.width//2 + 1, self.pos[0] + self.width//2 + self.safelim + 1): #the space to check South
                    if self.current[row, col] == 0: #South check
                        if self.dir == "E":
                            obsdir.append(["RIGHT", row - self.pos[0] - self.width//2])
                        elif self.dir == "W": 
                            obsdir.append(["LEFT", row - self.pos[0] - self.width//2])
                    
                    elif self.current[row, col] == 2: #South check
                        if self.dir == "E":
                            obsdir.append(["RIGHTC", row - self.pos[0] - self.width//2])
                        elif self.dir == "W": 
                            obsdir.append(["LEFTC", row - self.pos[0] - self.width//2])
                #     print("SOUTH", row, col)
                #     self.current[row, col] = 20
                # print()

            #checks in the East and West directions
            for row in range(self.pos[0] - self.width//2, self.pos[0] + self.width//2 + 1): #i refers to the index of the width to check while self.length refers to the length of the robot
                #checking west
                for col in range(self.pos[1] - self.length//2 - self.safelim, self.pos[1] -  self.length//2): 
                    if self.current[row, col] == 0:
                        if self.dir == "E":
                            obsdir.append(["BACK", self.pos[1] - self.length//2 - col])
                        elif self.dir == "W":
                            obsdir.append(["FRONT", self.pos[1] - self.length//2 - col])
                    
                    elif self.current[row, col] == 2:
                        if self.dir == "E":
                            obsdir.append(["BACKC", self.pos[1] - self.length//2 - col])
                        elif self.dir == "W":
                            obsdir.append(["FRONTC", self.pos[1] - self.length//2 - col])
                #     print("WEST", row, col)
                #     self.current[row, col] = 20
                # print()

                #checking east
                for col in range(self.pos[1] + self.length//2 + 1, self.pos[1] + self.length//2 + self.safelim + 1):
                    if self.current[row, col] == 0:
                        if self.dir == "E":
                            obsdir.append(["FRONT", col - self.pos[1] - self.length//2])
                        elif self.dir == "W":
                            obsdir.append(["BACK", col - self.pos[1] - self.length//2])
                    
                    elif self.current[row, col] == 2:
                        if self.dir == "E":
                            obsdir.append(["FRONTC", col - self.pos[1] - self.length//2])
                        elif self.dir == "W":
                            obsdir.append(["BACKC", col - self.pos[1] - self.length//2])
                #     print("EAST", row, col)
                #     self.current[row, col] = 20
                # print()
        # print(obsdir)

        #now we have a list of directions, but same directions might appear multiple times and with varying distanaces so
        #we want to (1) remove duplicated (2) only keep the ones with the smallest distances
        #recall that we saved each obstacle/direction as [direction, dist] in a nested list
        
        min_FRONT = self.safelim + 1 #just outside of scan range so it's definitely larger than all dist here
        min_BACK = self.safelim + 1
        min_LEFT = self.safelim + 1
        min_RIGHT = self.safelim + 1

        #This part checks each combination and updates the smallest value for that direction
        for obs in obsdir:
            if obs[0] == "FRONT":
                if obs[1] < self.safelim:
                    min_FRONT = obs[1]
            elif obs[0] == "BACK":
                if obs[1] < self.safelim:
                    min_BACK = obs[1]
            elif obs[0] == "LEFT":
                if obs[1] < self.safelim:
                    min_LEFT = obs[1]
            elif obs[0] == "RIGHT":
                if obs[1] < self.safelim:
                    min_RIGHT = obs[1]

        obs_clean = {} #a dictionary that returns the distance of detected obstacle with the direction as index eg. obs_clean["FRONT"]
        #This part updates the minimum value into the newly created blank dictionary
        if min_FRONT < self.safelim + 1:
            obs_clean["FRONT"] = min_FRONT
        if min_BACK < self.safelim + 1:
            obs_clean["BACK"] = min_BACK
        if min_LEFT < self.safelim + 1:
            obs_clean["LEFT"] = min_LEFT
        if min_RIGHT < self.safelim + 1:
            obs_clean["RIGHT"] = min_RIGHT


        #This part works the same as above but for the cleaning part detected

        min_FRONT = self.safelim + 1 #just outside of scan range so it's definitely larger than all dist here
        min_BACK = self.safelim + 1
        min_LEFT = self.safelim + 1
        min_RIGHT = self.safelim + 1

        #This part checks each combination and updates the smallest value for that direction
        for obs in obsdir:
            if obs[0] == "FRONTC":
                if obs[1] < self.safelim:
                    min_FRONT = obs[1]
            elif obs[0] == "BACKC":
                if obs[1] < self.safelim:
                    min_BACK = obs[1]
            elif obs[0] == "LEFTC":
                if obs[1] < self.safelim:
                    min_LEFT = obs[1]
            elif obs[0] == "RIGHTC":
                if obs[1] < self.safelim:
                    min_RIGHT = obs[1]

        
        #This part updates the minimum value into the newly created blank dictionary
        if min_FRONT < self.safelim + 1:
            obs_clean["FRONTC"] = min_FRONT
        if min_BACK < self.safelim + 1:
            obs_clean["BACKC"] = min_BACK
        if min_LEFT < self.safelim + 1:
            obs_clean["LEFTC"] = min_LEFT
        if min_RIGHT < self.safelim + 1:
            obs_clean["RIGHTC"] = min_RIGHT


        # print("Obstacles detected:", obs_clean, "Self facing:", self.dir)
        return obs_clean

     

    def pfindmap(self, start, end): #returns the sacred set of instructions to yeet back home
        dupmap = self.current.copy()
        dupmap[dupmap == 10] = 2
        dupmap[dupmap == 11] = 2
        dupmap[self.pos[0], self.pos[1]] = 10
        return pathfind.pfind(pathfind.thicc(dupmap, 2), start, end) #[row, col] form for start and end



if __name__ == "__main__":
    #sample map#
    SampleMap1 = np.genfromtxt("C:\\Users\\LQ\\Documents\\NTU\\Year 1 Special Sem\\M&T\\Raspberry Pi\\Making and Tinkering\\ObsTestMap(3_5).csv", delimiter = ",")

    """
    Initilising the sample start
    """
    Nmap = Map(100, [3,5]) #redundant but I like it here
    Nmap.current = SampleMap1
    Nmap.setpos(3, 5, "N") #ownself set
    Nmap.sethome(3, 5, "N") #same as above
    Nmap.expandcheck()
    print(Nmap.pos)
    print(Nmap.checksurr())
    Nmap.showcurrent(-1)

    
