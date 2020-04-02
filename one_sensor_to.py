# Import necessary libraries.
from Bluetin_Echo import Echo
import time
import pickle
from tkinter import *
import RPi.GPIO as GPIO
                                  
ROOT = Tk()
deg_sure 				= StringVar()
deg_result 				= StringVar()
LABEL_sure 			 	= Label(ROOT, textvariable=deg_sure 				,font=("Times", 25,'bold'), anchor="w",width=30) 
LABEL_result 			= Label(ROOT, textvariable=deg_result 				,font=("Times", 25,'bold'), anchor="w",width=30) 
# Define GPIO pin constants.
TRIGGER_PIN = 27
ECHO_PIN = 22
# Initialise Sensor with pins, speed of sound.
speed_of_sound = 315
echo = Echo(TRIGGER_PIN, ECHO_PIN, speed_of_sound)
# Measure Distance 5 times, return average.
samples = 1
# Take multiple measurements.
son = 1000
elapsedTime = 0.1 	# it is required to define an initial value

# handle the button event
counter = 0
def buttonEventHandler_ic(pin_ic):
	result = echo.read('cm', samples)
	with open('result.obj','wb') as dist:
		pickle.dump(result,dist)
	# Print result.
	if abs(son - result) > 1:
		print(result, 'cm')
		son = result
	elapsedTime = time.time() - ac_time
	deg_sure.set('# Frames/second:\t'+str(round(1/elapsedTime,2))+' fps')
	deg_sure.set('result:\t'+str(result))
def buttonEventHandler (pin):
    print ("handling button event")
#~ GPIO.add_event_detect(23,GPIO.FALLING)
#~ GPIO.add_event_callback(23,buttonEventHandler,100)
    #~ time.sleep(1) bu yorum satırıydı
    
#~ GPIO.add_event_detect(23,GPIO.RISING)
#~ GPIO.add_event_callback(23,buttonEventHandler,100)
    
while 1:
	ac_time = time.time() 
	time.sleep(.07)
	ROOT.update()					
	LABEL_sure.pack() 	# bu packleri while dışına alınca da aynı şekilde çalıştı nasılsa
	LABEL_result.pack()
	
	result = echo.read('cm', samples)
	with open('result.obj','wb') as dist:
		pickle.dump(result,dist)
	# Print result.
	if abs(son - result) > 1:
		print(result, 'cm')
		son = result
	elapsedTime = time.time() - ac_time
	deg_sure.set('# Frames/second:\t'+str(round(1/elapsedTime,2))+' fps')
	deg_sure.set('result:\t'+str(result))
	
#~ # Reset GPIO Pins.
echo.stop()
