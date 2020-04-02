
"""
	... kemal-i intizam ile bu kadar hassas duyguları ve hissiyatları ve gayet muntazam bu manevi latifeleri ve
batınî hasseleri bu cismimde derc etmekle beraber, gayet sanatlı bu cihazatı ve cevarihi ve hayat-ı insaniyece gayet
lüzumlu ve mükemmel bu kadar aletleri bu vücudumda kemal-i intizamla yaratmış.
"""
import time
import gor_class			# BUNUN İÇİNDE BAZI MODÜLLER IMPORT EDİLİYO. O YÜZDEN INIT MANASI FARZ-I AYN
import numpy as np
from imutils.video import VideoStream
import RPi.GPIO as GPIO
GPIO.setwarnings(False) 
#~ from matplotlib import pyplot as plt
#~ import imutils
import argparse
import cv2	# bunu gor_class'ta zaten import ettiğimizden burada tekrar import etmek süreyi uzatır mı diye düşünmüştüm
# ama elhamdülillah, tecrübe ettiğim gibi uzatmıyo, çünkü zaten imported
# import pyximport; pyximport.install() # it works only on pure Python modules. imiş
#~ import pickle
result = 40
#~ with open('result.obj','wb') as dist:
	#~ pickle.dump(result,dist)
import control
with open('balloon_config_file_webcam.cnf') as dosya:
	veri_web = dosya.readlines()
known_pix_oto_web = int(float(veri_web[6][14:-1]))
with open('balloon_config_file_picam.cnf') as dosya:
	veri_pi = dosya.readlines()
known_pix_oto_pi = int(float(veri_pi[6][14:-1]))

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-g", "--gui", type=int, default=1,
	help="whether or not gui is used. If you don't want to use gui, enter -1")
ap.add_argument("-i", "--image", type=int, default=1,
	help="whether or not image is used. If you don't want to use image, enter -1")
ap.add_argument("-b", "--both", type=int, default=1,
	help="whether or not both image and gui are used. If you don't want to use any of them, enter -1")
args = vars(ap.parse_args())

#~ GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                #~ bir alt satır normalde yorum satırı değildiie
GPIO.setmode(GPIO.BOARD)

GPIO_sensor_1_2 = 24 # front-right sensor
GPIO_sensor_3_4 = 21 # front-left sensor

GPIO.setup(GPIO_sensor_1_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(GPIO_sensor_3_4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# buraya kadar 2.8 saniye sürdü
 
# initialize the video stream and allow the camera sensor to warmup
#~ picam = VideoStream(usePiCamera=args["picamera"] < 0).start()

#~ https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html
#~ grab ve retrieve denenebilir coşkun daha hızlı demiş heralde multicamera varsa

#~ picam = VideoStream(usePiCamera=True,resolution=(480, 368)).start() # aç # dikkat PiCameraResolutionRounded diyebilir
picam = VideoStream(src=0).start() # (1280, 960) yazınca (640, 480) verdi yani yaklaşık 3 mp
webcam = VideoStream(src=1).start() # aç # resolution default olarak (320,240) (horiz,vert) default 160,120
# allow the camera to warmup
time.sleep(0.1)
#~ picam = cv2.VideoCapture(1)
#~ webcam = cv2.VideoCapture(0)

#~ time.sleep(2.0) # bu kritik mi acaba bilmiyorum
	
###################################################
	
#20.04 yenileme 
#GPIO port allocation for sensors (can be changed)
# interrupt 4 sensor için oldu
#a direction variable can be allocated
# to compare the real alarm.(gittiğimiz yönün aksinde sinyaln gelirse onu kale almayacaz
# çünkü motor u aniden çok zorlarız)
#bu degişkeni main de tutucağız.


#~ motorOutputPin2 = 38 # 32 33 35 (board) 12 13 19 (bcm)
#~ motorOutputPin1 = 29 

#~ pwm_yaz_sol = GPIO.PWM(motorOutputPin1, 500) # PWM has timing resolution of 1 us according to:
#~ pwm_yaz_sag = GPIO.PWM(motorOutputPin2, 500) # https://www.electronicwings.com/raspberry-pi/raspberry-pi-pwm-generation-using-python-and-c
# şimdi software pwm'i kullanıyoruz.
# bize eğer 1us (1000 Hz)'den daha yüksek bir resolution lazımsa hardware PWM'i kullanmak lazım. Onu araştırmadım.

#~ pwm_yaz_sol.start(pwmleft)
#~ pwm_yaz_sag.start(pwmright)


#~ pwm_yaz_sol.ChangeDutyCycle(pwmleft), pwm_yaz_sag.ChangeDutyCycle(pwmright)
flag = 0

def sensor3_4(habib):
	global flag
	flag = 1	
	print(flag)

	if(control.direction==1):
		
		GPIO.output(control.in1, GPIO.HIGH)
		GPIO.output(control.in2, GPIO.LOW)
		GPIO.output(control.in3, GPIO.HIGH)
		GPIO.output(control.in4, GPIO.LOW)	
			
		pwmright_interrupt = 0
		pwmleft_interrupt = 0
		control.pwm_yaz_sol.ChangeDutyCycle(pwmleft_interrupt)
		control.pwm_yaz_sag.ChangeDutyCycle(pwmright_interrupt)

		print (" pwmleft " , pwmleft_interrupt)
		print (" pwmright " , pwmright_interrupt)	
		#~ time.sleep(5)	
			
		while (GPIO.input(GPIO_sensor_3_4) == GPIO.HIGH):
			time.sleep(0.1)
		flag = 0	
	print('SONRA: ',flag)
			
def sensor1_2(habib):
	global flag
	flag = 1	
	print(flag)
	if(control.direction==2):
		
		GPIO.output(control.in1, GPIO.HIGH)
		GPIO.output(control.in2, GPIO.LOW)
		GPIO.output(control.in3, GPIO.LOW)
		GPIO.output(control.in4, GPIO.HIGH)	
			
		pwmright_interrupt = 0
		pwmleft_interrupt = 0
		control.pwm_yaz_sol.ChangeDutyCycle(pwmleft_interrupt)
		control.pwm_yaz_sag.ChangeDutyCycle(pwmright_interrupt)

		print (" pwmleft " , pwmleft_interrupt)
		print (" pwmright " , pwmright_interrupt)	
		#~ time.sleep(5)
			
		while (GPIO.input(GPIO_sensor_1_2) == GPIO.HIGH):
			time.sleep(0.2)
		flag = 0	
	print('SONRA: ',flag)

GPIO.add_event_detect(GPIO_sensor_1_2, GPIO.RISING, callback=sensor1_2)
GPIO.add_event_detect(GPIO_sensor_3_4, GPIO.RISING, callback=sensor3_4)

if args["gui"] == 1 and args["both"] == 1:
	from tkinter import StringVar,Label,Tk
	ROOT = Tk()
	deg_aci 				= StringVar()
	deg_distance_to_center 	= StringVar()
	deg_actual_distance 	= StringVar()
	deg_volt_sag 			= StringVar()
	deg_volt_sol 			= StringVar()
	deg_sure 				= StringVar()
	LABEL_aci 				 = Label(ROOT, textvariable=deg_aci 				,font=("Times", 25,'bold'), anchor="w",width=30)
	LABEL_distance_to_center = Label(ROOT, textvariable=deg_distance_to_center 	,font=("Times", 25,'bold'), anchor="w",width=30)
	LABEL_actual_distance 	 = Label(ROOT, textvariable=deg_actual_distance 	,font=("Times", 25,'bold'), anchor="w",width=30)
	LABEL_volt_sag 			 = Label(ROOT, textvariable=deg_volt_sag 			,font=("Times", 25,'bold'), anchor="w",width=30)
	LABEL_volt_sol 			 = Label(ROOT, textvariable=deg_volt_sol 			,font=("Times", 25,'bold'), anchor="w",width=30)
	LABEL_sure 			 	 = Label(ROOT, textvariable=deg_sure 				,font=("Times", 25,'bold'), anchor="w",width=30)
def webcam_func(webcam):
	#~ ret,webcam_resim = cap.read() # kapa
	webcam_resim = webcam.read() # aç
	global webcam_picture
	webcam_picture = gor_class.Goruntu(webcam_resim,'balloon_config_file_webcam.cnf',known_pix=240,known_dis=60,wrt_ground=55) # 1 ms falan
	global webcam_mask
	webcam_mask = webcam_picture.build_mask()
	#~ webcam_mask = imutils.rotate(webcam_mask,angle=180)
	kimse_yok_mu_webcam = webcam_picture.find_center(webcam_mask)
	webcam_picture.find_small_y_axis(fov_horizontal=49)		
	webcam_picture.find_vertical_angle(fov_vertical=37)	
	webcam_picture.find_distance_to_center()
	return kimse_yok_mu_webcam
def picam_func(picam):
	#~ picam_resim = im_frame.array # kapa
	picam_resim = picam.read() # aç
	global picam_picture
	picam_picture = gor_class.Goruntu(picam_resim,'balloon_config_file_picam.cnf',known_pix=240,known_dis=60,wrt_ground=55) # 1 ms falan
	global picam_mask
	picam_mask = picam_picture.build_mask()
	kimse_yok_mu_picam = picam_picture.find_center(picam_mask)
	picam_picture.find_small_y_axis(fov_horizontal=49) 	
	picam_picture.find_vertical_angle(fov_vertical=37)	
	picam_picture.find_distance_to_center()
	return kimse_yok_mu_picam
if args["gui"] == 1 and args["both"] == 1:
	LABEL_aci.pack()				
	LABEL_distance_to_center.pack()
	LABEL_actual_distance.pack()
	LABEL_volt_sag.pack()
	LABEL_volt_sol.pack()
	LABEL_sure.pack()
#~ fpss_toplam = 0
#~ countt = 0
per = 50
kimse_yok_mu = 1
elapsedTime = 0.1 	# it is required to define an initial value
cam_control = 0
sayy = 0
artik_yok = 0
while True: # aç
	try:
#~ for im_frame in cap.capture_continuous(rawCapture, format="bgr", use_video_port=True): # kapa
		if flag == 1:
			#~ GPIO.output(control.in1, GPIO.LOW)
			#~ GPIO.output(control.in2, GPIO.LOW)
			#~ GPIO.output(control.in3, GPIO.LOW)
			#~ GPIO.output(control.in4, GPIO.LOW)	
			pwmright_interrupt = 0
			pwmleft_interrupt = 0
			control.pwm_yaz_sol.ChangeDutyCycle(pwmleft_interrupt)
			control.pwm_yaz_sag.ChangeDutyCycle(pwmright_interrupt)
		else:

			ac_time = time.time() # actual time read
			if args["gui"] == 1 and args["both"] == 1:
				ROOT.update()
			#~ resim = imutils.resize(resim, width=400) # bunu uncomment etmek istiyosan imutils'i import et
			#~ resim = cv2.flip(resim,1) 
			#~ cv2.destroywindow('windowun_ismi')
			# 0 yapinca dikey, 1 yapınca yatay flip ediyo. Ama şuanki haliyle zaten hiç gerek yok. Bi de imutils'in kendi flip'i daha efficient olsa gerek
			#~ kimse_yok_mu = 0
			if cv2.waitKey(5) & 0xFF == ord('q'): # q ile çık programdan
				break
			if cam_control == 1 or picam_func(picam) == 1: # bir önceki frame'de webcam görmüşse veya şimdi picam görmediyse
				if webcam_func(webcam) == 1:
					kimse_yok_mu = 1
					cam_control = 0
					if kimse_yok_mu == 1:
						print('yok diyo!! ',sayy)
					sayy += 1
					if artik_yok == 1:
						continue
					control.dongu(yok_mu = 1)
					artik_yok = 1
					continue
				else:
					kimse_yok_mu = 0
					picture = webcam_picture
					mask = webcam_mask
					cam_control = 1
					tersmi_duzmu = 0
					artik_yok = 0
					#~ print(10*'\n')
			else:
				kimse_yok_mu = 0
				picture = picam_picture
				mask = picam_mask
				cam_control = 0
				tersmi_duzmu = 1
				artik_yok = 0
			
			actual_distance = picture.projection_of_distance_to_actual_place_of_balloon
			aci = picture.angle # in radians
			if tersmi_duzmu == 1:
				aci = -aci
			distance_to_center = picture.projection_of_distance_to_center
			goster_angle = aci*180/3.14
			
			pwmleft,pwmright = control.dongu(aci, actual_distance,kimse_yok_mu,tersmi_duzmu)
			# dongu() q returnlu olması ve burdan değerleri 
			# almamızın tek sebebi sonucu ekranda görme isteği. yani kaldırılabilir
			if args["both"] == 1 and args["gui"] == 1:
				deg_aci.set('angle:\t\t'+str(round(goster_angle,2))+' degrees')
				deg_distance_to_center.set('distance_to_center:'+str(round(distance_to_center,2))+' cm')
				deg_actual_distance.set('actual_distance:\t'+str(round(actual_distance,2))+' cm')
				deg_volt_sag.set('PWM_right:\t'+str(round(pwmright,2))+'%')
				deg_volt_sol.set('PWM_left:\t'+str(round(pwmleft,2))+'%')
				deg_sure.set('# Frames/second:\t'+str(round(1/elapsedTime,2))+' fps')
			if args["both"] == 1 and args["image"] == 1:
				mask75 = picture.rescale_frame(mask, percent=per)
				#~ th375 = picture.rescale_frame(picture.th3, percent=per)
				frame75 = picture.rescale_frame(picture.resim, percent=per)
				mask75_3_channel = cv2.cvtColor(mask75, cv2.COLOR_GRAY2BGR) 
				# COLOR_GRAY2BGR ile gray'i renkli yapmıyo, 3 channel'lı yapıyo sadece, concatanate yapabilmek için
				# print('shape: ',mask75.shape,'and',frame75.shape)
				ikisi= np.concatenate((mask75_3_channel,frame75), axis=0)
				#~ plt.hist(picture.resim.ravel(),256)
				#~ plt.title('histogram')
				cv2.imshow('Out', ikisi)
			elapsedTime = time.time() - ac_time
	except KeyboardInterrupt:
		cv2.destroyAllWindows()
		webcam.stop()
		picam.stop()	
		GPIO.cleanup()
cv2.destroyAllWindows()
webcam.stop() # aç
#~ webcam.release() # kapa
#~ picam.release() # kapa
picam.stop()	
GPIO.cleanup()
#~ raspistill -o image.jpg # picamera ile terminalden foto çekmek için
#~ fswebcam -d /dev/video0 -r 1920x1080 -S 0 -F 1 image10.jpg	# webcam ile terminalden foto çekmek için
#~ /opt/vc/bin/vcgencmd measure_temp	# rpi'nin core sıcaklığı
#~ nano ~/.bashrc yazarak dosyanın sonuna bi satır ekledim. default cd değişti




#yapılacak=distance'da geçmiş datayı tutup şimdiki ile kıyaslayıp çok farklıysa ignore
