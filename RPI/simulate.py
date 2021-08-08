"""
READ THIS

Since the checksurr() function is updated for direction, distance, and the detection of cleaned spots, this file will not work anymore
If you want to continue to work using this do rollback the version of mapping.py

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
Nmap.checksurr()
Nmap.showcurrent(1)
running = True
state = "start" #current state
pstate = None #previous state

while running:
    while state == "start" or state == "NORTH":
        if "FRONT" not in Nmap.checksurr(): #if front is clear
            Nmap.move(0, 1) #move forward, in this case north since it starts facing north, always, I guess
            state = "NORTH"
        else: #front not clear
            pstate = state
            state = "OBSTACLE"
        print(state)

    while state == "OBSTACLE": #in this state, the robot meets an obstacle, oh no, what should it do~~~?
        if pstate == "NORTH": #if previously going north
            if "FRONT" in Nmap.checksurr() and "RIGHT" in Nmap.checksurr(): #front and right blocked -> cannot rotate
                print("That's all folks, I'll do the rest another day")
                pstate = state
                state = "END"
            elif "FRONT" in Nmap.checksurr() and "RIGHT" not in Nmap.checksurr(): #right is clear!
                Nmap.move(0, -1) #reverse a bit
                Nmap.move(90, 0) #turn 90 from north to east
                # pstate = "NORTH" #this is to connect the directions, obstacle state has no effect on where the thing goes, might have to implement a pdir or something if needed
                state = "EAST"
        elif pstate == "EAST":
            if "RIGHT" not in Nmap.checksurr(): #if right is clear
                Nmap.move(0, -1)
                Nmap.move(90, 0) #turn 90 from east to south
                # pstate = state
                state = "SOUTH"
            else:
                print("Cannot turn right ggwp")
                state = "END"
        elif pstate == "SOUTH":
            if "FRONT" in Nmap.checksurr() and "LEFT" in Nmap.checksurr(): #front and left blocked -> cannot rotate
                print("That's all folks, I'll do the rest another day")
                pstate = state
                state = "END" 
            else: #left is clear!
                Nmap.move(0, -1)
                Nmap.move(270, 0) #turn 270 from south to east
                # pstate = state
                state = "EAST"
        print(state)

    while state == "EAST":
        for _ in range(5): #this is for moving how many steps        
            if "FRONT" not in Nmap.checksurr(): #if front is clear, which is East in this case
                Nmap.move(0, 1)
            else: #once kena obstacle within that few steps
                pstate = state
                state = "OBSTACLE"
            print(state)
        # if all(dir not in ["FRONT", "LEFT", "RIGHT", "BACK"] for dir in Nmap.checksurr()): #if front aka east is clear to turn
        if pstate == "NORTH":
            pstate = state
            state = "SOUTH"
            Nmap.move(90, 0)
        elif pstate == "SOUTH":
            pstate = state
            state = "NORTH"
            Nmap.move(270, 0)
        print(state)

    while state == "SOUTH":
        if "FRONT" not in Nmap.checksurr(): #if front is clear
            Nmap.move(0, 1) #move forward, in this case south
            state = "SOUTH"
        else: #front not clear
            pstate = state
            state = "OBSTACLE"
        print(state)

    if state == "END":
        running = False
        Nmap.showcurrent(-1)
                
            
                




