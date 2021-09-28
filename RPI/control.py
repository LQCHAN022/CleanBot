"""
Aim to use keyboard to control to demonstrate capabilities
"""
import keyboard

while True:
    if(keyboard.is_pressed("w")):
        print("w")
        while(keyboard.is_pressed("w")):
            pass
        else:
            print("w released")
    elif(keyboard.is_pressed("a")):
        print("a")
        while(keyboard.is_pressed("a")):
            pass
        else:
            print("a released")
    elif(keyboard.is_pressed("s")):
        print("s")
        while(keyboard.is_pressed("s")):
            pass
        else:
            print("s released")
    elif(keyboard.is_pressed("d")):
        print("d")
        while(keyboard.is_pressed("d")):
            pass
        else:
            print("d released")
