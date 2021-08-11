"""
Tasks:
Implement logic for when cleaned portion is encoutered
When this happens, attempt to shift right by std amount the hug cleaned

When faced with stuck, hug obstacle
When no obstacle to hug, go back to start


Implement pathfinding
When to stop, by coutns or time or coverage of area or rate of cleaning ie. unknown change to clean in a set timing



"""


from mapping import Map
import numpy as np
import time
import matplotlib.pyplot as plt

#sample map#
SampleMap1 = np.genfromtxt("C:\\Users\\LQ\\Documents\\NTU\\Year 1 Special Sem\\M&T\\Raspberry Pi\\Making and Tinkering\\LabMap1.csv", delimiter = ",")

"""
Initilising the sample start
"""
Nmap = Map(100, [3,5]) #redundant but I like it here
Nmap.current = SampleMap1
# Nmap.showcurrent(-1)
Nmap.setpos(97, 3, "N") #ownself set
Nmap.sethome(97, 3, "N") #same as above
Nmap.expandcheck()
print(Nmap.checksurr())
Nmap.showcurrent(1)
running = True
state = "start" #current state
pstate = None #previous state

while running:
    while state == "start" or state == "NORTH":
        print(Nmap.checksurr().get("LEFT", 5))
        if Nmap.checksurr().get("LEFT", 5) < 2 or Nmap.checksurr().get("LEFTC", 5) < 2: #if left side got wall or cleaned
            if Nmap.checksurr().get("FRONT", 2) > 1: #if front is clear till the edge
                Nmap.move(0, 1) #move forward, in this case north since it starts facing north, always, I guess
                state = "NORTH"
            else: #front not clear
                pstate = state
                state = "OBSTACLE"
        
        else:
            pstate = "NORTH"
            state = "HUG"

    while state == "OBSTACLE": #in this state, the robot meets an obstacle, oh no, what should it do~~~?
        if pstate == "NORTH": #if previously going north
            while Nmap.checksurr().get("BACK", 2) > 1: #while back has space to reverse
                if Nmap.checksurr().get("FRONT", 5) < 4: #if Front clearance less than 4
                    Nmap.move(0, -1) #reverse
                else: #enough space alr
                    break
            if Nmap.checksurr().get("RIGHT", 5) >= 4 : #if right is clear
                Nmap.move(90, 0) #turn 90 from north to east
                state = "EAST"
            else: #if right no space to turn reverse until there is
                while Nmap.checksurr().get("BACK", 2) > 1: #while back has space to reverse
                    if Nmap.checksurr().get("FRONT", 5) < 4: #if Front clearance less than 4
                        Nmap.move(0, -1) #reverse
                    else: #enough space alr
                        break

        elif pstate == "EAST":
            while Nmap.checksurr().get("BACK", 2) > 1: #while back has space to reverse
                if Nmap.checksurr().get("FRONT", 5) < 4: #if Front clearance less than 4
                    Nmap.move(0, -1) #reverse
                else: #enough space alr
                    break
            if Nmap.checksurr().get("RIGHT", 5) >= 4 : #if right is clear
                Nmap.move(90, 0) #turn 90 from EAST to SOUTH
                state = "SOUTH"
            else: #if right no space to turn reverse until there is
                while Nmap.checksurr().get("BACK", 2) > 1: #while back has space to reverse
                    if Nmap.checksurr().get("FRONT", 5) < 4: #if Front clearance less than 4
                        Nmap.move(0, -1) #reverse
                    else: #enough space alr
                        break

        elif pstate == "SOUTH":
            while Nmap.checksurr().get("BACK", 2) > 1: #while back has space to reverse
                if Nmap.checksurr().get("FRONT", 5) < 4: #if Front clearance less than 4
                    Nmap.move(0, -1) #reverse
                else: #enough space alr
                    break
            if Nmap.checksurr().get("RIGHT", 5) >= 4 : #if right is clear
                Nmap.move(90, 0) #turn 90 from EAST to SOUTH
                state = "WEST"
            else: #if right no space to turn reverse until there is
                while Nmap.checksurr().get("BACK", 2) > 1: #while back has space to reverse
                    if Nmap.checksurr().get("FRONT", 5) < 4: #if Front clearance less than 4
                        Nmap.move(0, -1) #reverse
                    else: #enough space alr
                        break
        
        elif pstate == "WEST":
            while Nmap.checksurr().get("BACK", 2) > 1: #while back has space to reverse
                if Nmap.checksurr().get("FRONT", 5) < 4: #if Front clearance less than 4
                    Nmap.move(0, -1) #reverse
                else: #enough space alr
                    break
            if Nmap.checksurr().get("RIGHT", 5) >= 4 : #if right is clear
                Nmap.move(90, 0) #turn 90 from EAST to SOUTH
                state = "NORTH"
            else: #if right no space to turn reverse until there is
                while Nmap.checksurr().get("BACK", 2) > 1: #while back has space to reverse
                    if Nmap.checksurr().get("FRONT", 5) < 4: #if Front clearance less than 4
                        Nmap.move(0, -1) #reverse
                    else: #enough space alr
                        break

    while state == "HUG": #this state will persist until left side hugs something

        """
        This part is buggy af, especially in practical use. There's the interaction between the clearance when no left detected 
        and also from obstacle detected need to sort it out
        """

        #generally will just rotate left, go forward a bit
        if Nmap.checksurr().get("FRONT", 5) >= 4: #if front got space
            Nmap.move(270, 0) #rotate CCW
            if pstate == "NORTH":
                state = "WEST"
            elif pstate == "WEST":
                    state = "SOUTH"
            elif pstate == "SOUTH":
                    state = "EAST"
            elif pstate == "EAST":
                    state = "NORTH"
        else:

            Nmap.move(90, 0) #The "hole" detected too tight to turn into, treat that as an obstacle instead
            if pstate == "NORTH":
                state = "EAST"
            elif pstate == "EAST":
                    state = "SOUTH"
            elif pstate == "SOUTH":
                    state = "WEST"
            elif pstate == "WEST":
                    state = "NORTH"



    while state == "EAST":
        if Nmap.checksurr().get("FRONT", 2) > 1: #if front is clear till the edge
            Nmap.move(0, 1) #move forward, in this case EAST since it's facing EAST
            state = "EAST"
        else: #front not clear
            pstate = state
            state = "OBSTACLE"
        print(state)

    while state == "SOUTH":
        if Nmap.checksurr().get("FRONT", 2) > 1: #if front is clear till the edge
            Nmap.move(0, 1) #move forward, in this case EAST since it's facing EAST
            state = "SOUTH"
        else: #front not clear
            pstate = state
            state = "OBSTACLE"
        print(state)
    
    while state == "WEST":
        if Nmap.checksurr().get("FRONT", 2) > 1: #if front is clear till the edge
            Nmap.move(0, 1) #move forward, in this case EAST since it's facing EAST
            state = "WEST"
        else: #front not clear
            pstate = state
            state = "OBSTACLE"
        print(state)

    if state == "END":
        running = False
        Nmap.showcurrent(-1)
                
            
                




