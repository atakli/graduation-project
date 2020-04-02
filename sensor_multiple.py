# Import necessary libraries.
from Bluetin_Echo import Echo
import time                                                         
 
# Define GPIO pin constants.
TRIGGER_PIN_1 = 4
ECHO_PIN_1 = 17

TRIGGER_PIN_2 = 27 # 
ECHO_PIN_2 = 22 # 

# Initialise Sensor with pins, speed of sound.
#~ speed_of_sound = 315
echo = [Echo(TRIGGER_PIN_1, ECHO_PIN_1), Echo(TRIGGER_PIN_2, ECHO_PIN_2)]
# Measure Distance 5 times, return average.
samples = 1
# Take multiple measurements.
son1 = 1000
#~ while 1:
	#~ time.sleep(.07)
	#~ result = echo.read('cm', samples)
	#~ # Print result.
	#~ if abs(son - result) > 2:
		#~ print(result, 'cm')
		#~ son = result
def main():
	#time.sleep(0.006)
	while 1:
		for counter in range(0,len(echo)):
			result = echo[counter].read('cm',3)
			if abs(son1 - result1) > 2:
				print('Sensor {} - {} cm'.format(counter,round(result,2)))
				#~ son1= 
	echo[0].stop()	
# Reset GPIO Pins.
#~ echo.stop()
if __name__ == '__main__':
	main()
