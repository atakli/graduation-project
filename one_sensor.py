# Import necessary libraries.
from Bluetin_Echo import Echo
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
import argparse                                  
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-g", "--gui", type=int, default=1,
	help="whether or not gui is used. If you don't want to use gui, enter -1")
args = vars(ap.parse_args())
if args["gui"] == 1:
	from tkinter import StringVar,Label,Tk
	ROOT = Tk()
	deg_sure 				= StringVar()
	deg_result 				= StringVar()
	LABEL_sure 			 	= Label(ROOT, textvariable=deg_sure 				,font=("Times", 25,'bold'), anchor="w",width=30) 
	LABEL_result 			= Label(ROOT, textvariable=deg_result 				,font=("Times", 25,'bold'), anchor="w",width=30) 
# Define GPIO pin constants.
TRIGGER_PIN_1 = 27
ECHO_PIN_1 = 22
TRIGGER_PIN_2 = 4
ECHO_PIN_2 = 17


#bunlar yanlış diğerleri ile aynı şeyi yazdık
TRIGGER_PIN_4 = 2
ECHO_PIN_4 = 3
TRIGGER_PIN_3 =15
ECHO_PIN_3 = 14



control_pin_1_2=25
control_pin_3_4=11

GPIO.setup(control_pin_3_4, GPIO.OUT)
GPIO.setup(control_pin_1_2, GPIO.OUT)

# Initialise Sensor with pins, speed of sound.
speed_of_sound = 315
echo_1 = Echo(TRIGGER_PIN_1, ECHO_PIN_1, speed_of_sound)
echo_2 = Echo(TRIGGER_PIN_2, ECHO_PIN_2, speed_of_sound)
echo_3 = Echo(TRIGGER_PIN_3, ECHO_PIN_3, speed_of_sound)
echo_4 = Echo(TRIGGER_PIN_4, ECHO_PIN_4, speed_of_sound)
# Measure Distance 5 times, return average.
samples = 3
# Take multiple measurements.
son = 1000
elapsedTime = 0.1 	# it is required to define an initial value
result=10000
result_1=10000
result_1_old=10000
result_2=10000
result_2_old=10000
result_3=10000
result_3_old=10000
result_4=10000
result_4_old=10000
counter=1
if args["gui"] == 1:			
	LABEL_sure.pack() 
	LABEL_result.pack()
#~ (echo_1,echo_2,echo_3,echo_4): 
    
while 1:

	for echo in (echo_1,echo_2,echo_3,echo_4):
		ac_time = time.time() 
		time.sleep(.07)
		if args["gui"] == 1:
			ROOT.update()		
		
		#~ global result
		
		result = echo.read('cm', samples)
		
		#~ if abs(result1 - result) > 2:
			#~ print(result, 'cm')
			#~ result = result1
		#~ if(counter==1):
			#~ result_1= echo.read('cm', samples)
			
			#~ if abs(result_1 - result_1_old) > 2:
				#~ result=result_1
				
			#~ result_1_old=result	
		#~ elif(counter==2):
			#~ result_2 = echo.read('cm', samples)
			
			#~ if abs(result_2 - result_2_old) > 2:
				#~ result=result_2
				
			#~ result_2_old=result					
			
		#~ elif(counter==3):
			#~ result_3 = echo.read('cm', samples)
			
			#~ if abs(result_3 - result_3_old) > 2:
				#~ result=result_1
				
			#~ result_3_old=result	
							
		#~ elif(counter==4):
			#~ result_4 = echo.read('cm', samples)
					
			#~ if abs(result_4 - result_4_old) > 2:
				#~ result=result_4
				
			#~ result_4_old=result			
		
		if result < 30:
			if result ==0:
				pass
			else:	
				if(counter==1):
					GPIO.output(control_pin_1_2, GPIO.HIGH)
				elif(counter==2):
					GPIO.output(control_pin_1_2, GPIO.HIGH)
				elif(counter==3):
					GPIO.output(control_pin_3_4, GPIO.HIGH)
				elif(counter==4):
					GPIO.output(control_pin_3_4, GPIO.HIGH)
				#~ print(counter," .result = ",result)
					
		else:
			if(counter==1):
				GPIO.output(control_pin_1_2, GPIO.LOW)
			elif(counter==2):
				GPIO.output(control_pin_1_2, GPIO.LOW)
			elif(counter==3):
				GPIO.output(control_pin_3_4, GPIO.LOW)
			elif(counter==4):
				GPIO.output(control_pin_3_4, GPIO.LOW)
			#~ print(counter," .result = ",result)
		if args["gui"] == 1:
			deg_sure.set('# Frames/second:\t'+str(round(1/elapsedTime,2))+' fps')
			deg_sure.set(str(counter)+' .result:\t'+str(round(result,2)))
		counter += 1
		if counter == 5:
			counter = 1
		elapsedTime = time.time() - ac_time
#~ # Reset GPIO Pins.
echo_1.stop()
echo_2.stop()
echo_3.stop()
echo_4.stop()





