from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#statemachine in software voor pauze en shutdown

#Distance between sub system form start in mm
Distance = 1



#General motor setup
M1_0 = 14   # Controling the microstepping
M1_1 = 15   # Controling the microstepping
M1_2 = 18   # Controling the microstepping
CW = 1      # Clockwise Rotation
CCW = 0     # Counterclockwise Rotation
SPR = 200   # Steps per Revolution (360 / 1.8)

GPIO.setup(M1_0, GPIO.OUT)
GPIO.setup(M1_1, GPIO.OUT)
GPIO.setup(M1_2, GPIO.OUT)


#Motor Sensor 1 (left) GPIO pins
DIR_M_S_Left = 20   # Direction
STEP_M_S_Left = 21  # Step

GPIO.setup(DIR_M_S_Left, GPIO.OUT)
GPIO.setup(STEP_M_S_Left, GPIO.OUT)


#Motor Sensor 2 (right) GPIO pins
DIR_M_S_Right = 16   # Direction
STEP_M_S_Right = 21  # Step

GPIO.setup(DIR_M_S_Right, GPIO.OUT)
GPIO.setup(STEP_M_S_Right, GPIO.OUT)


#Motor Belt GPIO pins
DIR_M_B = 9
STEP_M_B = 12
M2_0 = 25
M2_1 = 8
M2_2 = 7

GPIO.setup(DIR_M_B, GPIO.OUT)
GPIO.setup(STEP_M_B, GPIO.OUT)
GPIO.setup(M2_0, GPIO.OUT)
GPIO.setup(M2_1, GPIO.OUT)
GPIO.setup(M2_2, GPIO.OUT)


#Relay GPIO pins
BlOWER_LEFT = 2   #Activating the left blower
BLOWER_RIGHT = 3  #Activating the right blower
PISTON_OUT = 23   #Allowing the piston to move out
MOTOR_POWER = 24  #Allowing the motors to have power

GPIO.setup(BlOWER_LEFT, GPIO.OUT)
GPIO.setup(BLOWER_RIGHT, GPIO.OUT)
GPIO.setup(PISTON_OUT, GPIO.OUT)
GPIO.setup(MOTOR_POWER, GPIO.OUT)


#Switches GPIO pins
S_BELT_END = 5
S_BELT_START = 6
S_SENSOR_LEFT = 13
S_SENSOR_RIGHT = 19
S_DISPENSER = 26

GPIO.setup(S_BELT_END, GPIO.IN)
GPIO.setup(S_BELT_START, GPIO.IN)
GPIO.setup(S_SENSOR_LEFT, GPIO.IN)
GPIO.setup(S_SENSOR_RIGHT, GPIO.IN)
GPIO.setup(S_DISPENSER, GPIO.IN)


#IR Sensor GPIO pin
IR_Sensor = 11

GPIO.setup(IR_Sensor, GPIO.IN)


# Setting the resolution and timing of the steppers
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}

SENSOR_MODE = (M1_0, M1_1, M1_2)   # Microstep Resolution GPIO Pins
GPIO.setup(SENSOR_MODE, GPIO.OUT)
GPIO.output(SENSOR_MODE, RESOLUTION['Half'])
step_count_Sensor = SPR * 2
delay_Sensor = .01 

BELT_MODE = (M2_0, M2_1, M2_2)   # Microstep Resolution GPIO Pins
GPIO.setup(BELT_MODE, GPIO.OUT)
GPIO.output(BELT_MODE, RESOLUTION['Full'])
step_count_Belt = SPR * 1
delay_Belt = .00045 / 1


def Calibration_Sensor_Left():
    #Calibration of the left sensor
    GPIO.output(DIR_M_S_Left, CW)
    while True:
        if (GPIO.input(S_SENSOR_LEFT) == False):
            GPIO.output(STEP_M_S_Left, GPIO.HIGH)
            sleep(delay_Sensor)
            GPIO.output(STEP_M_S_Left, GPIO.LOW)
            sleep(delay_Sensor)
            
        elif (GPIO.input(S_SENSOR_LEFT) == True):
            break:


def Calibration_Sensor_Right():
    #Calibration of the right sensor
    GPIO.output(DIR_M_S_Right, CCW)
    while True:
        if (GPIO.input(S_SENSOR_RIGHT) == False):
            GPIO.output(STEP_M_S_Right, GPIO.HIGH)
            sleep(delay_Sensor)
            GPIO.output(STEP_M_S_Right, GPIO.LOW)
            sleep(delay_Sensor)
            
        elif (GPIO.output(S_SENSOR_RIGHT) == True):
            break:


def Calibration_Belt():
    SWITCH_END = 0
    Total_Steps_Belt = 0
    GPIO.output(DIR_M_B, CW)
    
    while True:
        if ((GPIO.input(S_BELT_END) == False) and (SWITCH_END == 0)):
            GPIO.output(STEP_M_S_Right, GPIO.HIGH)
            sleep(delay_Sensor)
            GPIO.output(STEP_M_S_Right, GPIO.LOW)
            sleep(delay_Sensor)
            
        elif ((GPIO.input(S_BELT_END) == True) and (SWITCH_END == 0)):
            SWITCH_END = 1
            GPIO.output(DIR_M_B, CCW)
            sleep(delay_Sensor)
        
        elif ((GPIO.input(S_BELT_START) == False) and (SWITCH_END == 1)):
            GPIO.output(STEP_M_B, GPIO.HIGH)
            sleep(delay_Belt)
            GPIO.output(STEP_M_B, GPIO.LOW)
            sleep(delay_Belt)
            Total_Steps_Belt =+ 1
            
        elif ((GPIO.input(S_BELT_START) == True) and (SWITCH_END == 1)):
            break:
        
    return Total_Steps_Belt


def Calibration_Dispenser():
    while True:
        if (GPIO.input(S_DISPENSER) == False):
            GPIO.output(PISTON_OUT, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(PISTON_OUT, GPIO.LOW)
            
        elif (GPIO.input(S_DISPENSER) == True):
            break:


def Calibration_Blower():
    GPIO.output(BlOWER_LEFT, HIGH)
    sleep(1)
    GPIO.output(BlOWER_LEFT, LOW)
    sleep(2)
    
    GPIO.output(BlOWER_RIGHT, HIGH)
    sleep(1)
    GPIO.output(BlOWER_RIGHT, LOW)


def Sensor_TO_0():
    GPIO.output(DIR_M_S_Left, CW)
    GPIO.output(DIR_M_S_Right, CCW)
    
    while True:
        if ((GPIO.input(S_SENSOR_LEFT) == False) and (GPIO.input(S_SENSOR_RIGHT) == False)):
            GPIO.output(STEP_M_S_Right, GPIO.HIGH)
            GPIO.output(STEP_M_S_Left, GPIO.HIGH)
            sleep(delay_Sensor)
            GPIO.output(STEP_M_S_Right, GPIO.LOW)
            GPIO.output(STEP_M_S_Left, GPIO.LOW)
            sleep(delay_Sensor)
            
        elif ((GPIO.input(S_SENSOR_LEFT) == False) and (GPIO.input(S_SENSOR_RIGHT) == True)):
            GPIO.output(STEP_M_S_Left, GPIO.HIGH)
            sleep(delay_Sensor)
            GPIO.output(STEP_M_S_Left, GPIO.LOW)
            sleep(delay_Sensor)
        
        elif ((GPIO.input(S_SENSOR_LEFT) == True) and (GPIO.input(S_SENSOR_RIGHT) == False)):
            GPIO.output(STEP_M_S_Right, GPIO.HIGH)
            sleep(delay_Sensor)
            GPIO.output(STEP_M_S_Right, GPIO.LOW)
            sleep(delay_Sensor)
            
        elif ((GPIO.input(S_SENSOR_LEFT) == True) and(GPIO.input(S_SENSOR_RIGHT) == True)):
            break:


def Sensor_TO_200():
    GPIO.output(DIR_M_S_Left, CCW)
    GPIO.output(DIR_M_S_Right, CW)
    steps_for_200 = 111    #111 steps for roting ~200 degrees
    
    for x in range(steps_for_200):
        GPIO.output(STEP_M_S_Right, GPIO.HIGH)
        GPIO.output(STEP_M_S_Left, GPIO.HIGH)
        sleep(delay_Sensor)
        GPIO.output(STEP_M_S_Right, GPIO.LOW)
        GPIO.output(STEP_M_S_Left, GPIO.LOW)
        sleep(delay_Sensor)


def Belt_TO_Measure(Total_Steps_Belt):
    GPIO.output(DIR_M_B, CW)
    pass


def Belt_TO_Blower(Total_Steps_Belt):
    GPIO.output(DIR_M_B, CCW)
    pass


def Belt_TO_Dispenser(Total_Steps_Belt):
    GPIO.output(DIR_M_B, CCW)
    pass


def Dispenser():
    while True:
        if(IR_Sensor == False):
            GPIO.output(PISTON_OUT, HIGH)
            sleep(0.5)
            GPIO.output(PISTON_OUT, LOW)
            sleep(0.5)
            break:


def Blower_Left():
    GPIO.output(BlOWER_LEFT, HIGH)
    sleep(0.5)
    GPIO.output(BlOWER_LEFT, LOW)


def Blower_Right():
    GPIO.output(BlOWER_RIGHT, HIGH)
    sleep(0.5)
    GPIO.output(BlOWER_RIGHT, LOW)
    
    
GPIO.output(MOTOR_POWER, GPIO.HIGH)
Calibration_Sensor_Left()
Calibration_Sensor_Right()
Calibration_Belt()



while True:
    

#GPIO.cleanup()
