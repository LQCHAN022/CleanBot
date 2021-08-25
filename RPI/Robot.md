# Documentation for Robot class

## Robot() `class`
`Robot Robot(arduinoSensor, arduinoMove, arduinoPump)`
#### Description
* Instantiates a Robot object
#### Parameters
* arduinoSensor: serial.Serial object linked to the Sensor Arduino
* arduinoMove: serial.Serial object linked to the Movment/Motor Arduino
* arduinoPump: serial.Serial object linked to the Pump Arduino
#### Returns
* Robot class object

## move() `method`
`void self.move(dir, dist = 20700)`
#### Description
* Moves the robot either Forward, Reverse, or Rotate 90 degrees in the clockwise or anti-clockwise direction
#### Parameters
* dir: Direction of movement, can take the values of:
  * 0: Forward
  * 180: Reverse
  * 90: Clockwise 90 degrees
  * 270: Anti-clockwise 90 degrees
* dist: Distance in steps to move, view steps conversion file to convert to distance moved/angle rotated
  * dist = -1: If dir = 0 or dir = 180, Robot will move indefinitely until stopped, else pass
  * dist > 0: If dir = 0 or dir = 180, Robot will move in set direction for *dist* steps
  * dir = 90 or dir = 270: dist will have no effect
#### Returns
* void

## stop()`method`
`void self.stop()`
#### Description
* Stops the robot immediately
#### Parameters
* None
#### Returns
* void

## cleanon()`method`
`void self.cleanon(pwm = 100, sps = 1000)`
#### Description
* Starts the roller and the pump
#### Parameters
* pwm: Duty cycle of the pump, ranges from 0 - 100
* sps: Steps per second of the roller motor, limited to limit set in StepperDriver.ino
#### Returns
* void

## cleanoff()`method`
`void self.cleanoff()`
#### Description
* Stops the cleaning process, which includes pump and roller motor
#### Parameters
* None
#### Returns
* void

## stopall()`method`
`void self.stopall()`
#### Description
* Stops everything, movement and cleaning
#### Parameters
* None
#### Returns
* void

## read()`method`
`void self.read(arduino)`
#### Description
* Reads from the specified arduino and updates the respective attributes
#### Parameters
* arduino: specifies the arduino to read from and updates the respective attributes (see *Attributes*)
  * "SENSOR" updates:
    * `self.Echo`: Echo distances in each direction
    * `self.Accel`: The angles in the X, Y and Z direction
    * `self.Bump`: Bump status of the bumper
    * `self.B1`, `self.B2`: Toggle state of button
  * "MOVE" updates:
    *  `self.dir`: Updates the direction that the Robot is facing if a turn is completed
    *  `self.rotate`: Updates whether the Robot has finished its rotation
    *  `self.Delta`: Updates the coordinates based on Forward or Reverse movement
      * Currently this depends purely on the number of steps passed to the motors
      * The Delta is in the number of grids, where each grid is 5 cm
      * Coordinates takes its starting point as origin
  * "PUMP" updates:
    * None    
#### Returns
* void

## scan()`method`
`void.scan()`
#### Description
* `read()` both `"SENSOR"` and `"MOVE"` and updates the map of: 
  * Obstacles and clear areas in the four directions
  * Own position on the map according to `self.Delta`
#### Parameters
* None
#### Returns
* void

## state`attribute`
`String self.state`
#### Description
* Movement that the Robot is doing now
* Takes values of `FRONT`, `BACK`, `RIGHT`, `LEFT`, `ETURN`, `QTURN`, `STOP`

## rotate`attribute`
`Boolean self.rotate`
#### Description
* Shows if rotation is completed
* False when rotation is starting, True when rotation is completed

## Echo`attribute`
`dict self.Echo`
#### Description
* Dictionary that returns direction to obstacle `int dist` in cm depending on direction `FRONT`, `BACK`, `RIGHT`, `LEFT`

## Accel`attribute`
`dict self.Accel`
#### Description
* Dictionary that returns angles in different axis `float angle` in degrees depending on axis `X`, `Y`, `Z`

## Bump`attribute`
`String self.Bump`
#### Description
* Status of bumper, takes either `CLEAR` or `BUMP`

## Bx`attribute`
`Boolean self.Bx`
#### Description
* x in range(1, 3) for total of 2 buttons
* Takes values of 0 or 1
