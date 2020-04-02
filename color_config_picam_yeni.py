# import ConfigParser
import cv2
import numpy as np
import time
import gor_class
from imutils.video import VideoStream
import imutils
from tkinter import StringVar,Label,Tk
per = 50
picam = VideoStream(src=1).start()
#~ try:
	#~ from picamera.array import PiRGBArray as PiRGBArray
	#~ from picamera import PiCamera as PiCamera
#~ except ImportError:
	#~ print("picamera not installed - please install if running on RPI")
#~ ROOT = Tk()
#~ deg_aci 				= StringVar()
#~ deg_sure 				= StringVar()
#~ LABEL_aci 				 = Label(ROOT, textvariable=deg_aci 				,font=("Times", 25,'bold'), anchor="w",width=30)
#~ LABEL_sure 			 	 = Label(ROOT, textvariable=deg_sure 				,font=("Times", 25,'bold'), anchor="w",width=30)
#~ LABEL_aci.pack()
#~ LABEL_sure.pack()
#~ len_cisim = 22
class BalloonConfig:
	def __init__(self):
		with open('balloon_config_file_picam.cnf') as dosya:
			self.veri = dosya.readlines()
	def rescale_frame(self,resim_to_be_rescaled, percent=75):
		width = int(resim_to_be_rescaled.shape[1] * percent/ 100)
		height = int(resim_to_be_rescaled.shape[0] * percent/ 100)
		dim = (width, height)
		return cv2.resize(resim_to_be_rescaled, dim, interpolation = cv2.INTER_AREA)
	def nothing(self,x):
		pass
	def save_callback(self,x):
		if x ==1:
			with open('balloon_config_file_picam.cnf','w') as dosya:
				dosya.writelines(['H Low = ',str(self.hul),'\n',			
								'H High = ',str(self.huh),'\n',
								'S Low = ',str(self.sal),'\n',		
								'S High = ',str(self.sah),'\n',		
								'V Low = ',str(self.val),'\n',		
								'V High = ',str(self.vah),'\n',
								'KNOWN_PIXEL = ',str(self.horizontal_pixels_of_balloon_ic),'\n'])
								#~ 'angle = ',str(self.angle),'\n'])		
			print("Saved colour filters to config file!")		
	def create_sliders(self):
		cv2.namedWindow('Bars', flags = cv2.WINDOW_AUTOSIZE)
		cv2.resizeWindow('Bars', 500,400)
		cv2.createTrackbar('H Low', 'Bars', 0, 179, self.nothing)
		cv2.createTrackbar('H High', 'Bars', 0, 179, self.nothing)
		cv2.createTrackbar('S Low', 'Bars', 0, 255, self.nothing)
		cv2.createTrackbar('S High', 'Bars', 0, 255, self.nothing)
		cv2.createTrackbar('V Low', 'Bars', 0, 255, self.nothing)
		cv2.createTrackbar('V High', 'Bars', 0, 255, self.nothing)
		cv2.createTrackbar('Save', 'Bars', 0, 1, self.save_callback)
		# cv2.createTrackbar('Area', 'Bars', 0, 200000, self.nothing)
	def set_initials_of_sliders(self):
		cv2.setTrackbarPos('H Low', 'Bars',  int(self.veri[0][8:-1]))			# 33)#
		cv2.setTrackbarPos('H High', 'Bars', int(self.veri[1][9:-1]))			# 82)#
		cv2.setTrackbarPos('S Low', 'Bars', int(self.veri[2][8:-1]))			# 82)#
		cv2.setTrackbarPos('S High', 'Bars', int(self.veri[3][9:-1]))		# 255)#
		cv2.setTrackbarPos('V Low', 'Bars', int(self.veri[4][8:-1]))			# 94)#
		cv2.setTrackbarPos('V High', 'Bars', int(self.veri[5][9:-1]))		# 255)#
		cv2.setTrackbarPos('Save', 'Bars', 0)
		# cv2.setTrackbarPos('Area', 'Bars', 10000)		#165000
	def get_values_from_slider_positions(self):
		self.hul = cv2.getTrackbarPos('H Low', 'Bars')
		self.huh = cv2.getTrackbarPos('H High', 'Bars')
		self.sal = cv2.getTrackbarPos('S Low', 'Bars')
		self.sah = cv2.getTrackbarPos('S High', 'Bars')
		self.val = cv2.getTrackbarPos('V Low', 'Bars')
		self.vah = cv2.getTrackbarPos('V High', 'Bars')
		# self.save = cv2.getTrackbarPos('Save', 'Bars')
		# area_bared = cv2.getTrackbarPos('Area', 'Bars')
		low = np.array([self.hul, self.sal, self.val])
		high = np.array([self.huh, self.sah, self.vah])
		return low,high#,save_or_not#,area_bared
	def find_center(self):
		cnts = cv2.findContours(self.mask_ic.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		center = None
		#~ print(len(cnts))		
		yok_mu = 0
		radius = 0	
		if len(cnts) > 0:
			# find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)

			#~ ellipse = cv2.fitEllipse(c)
			#~ cv2.ellipse(self.frame,ellipse,(0,255,0),2)	# denenebilir
			
			M = cv2.moments(c)

			try:
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			except ZeroDivisionError:
				center = (0,0)
			(self.center_x,self.center_y) = center
			# only proceed if the radius meets a minimum size
			if radius > 10: # eğer balonun radius'u 10'dan büyükse algıla, yoksa algılama çünkü o şey balon olmayabilir
				cv2.circle(self.frame, (int(x), int(y)), int(radius), (0, 255, 255), 2) # balonun çevresini çizer
				cv2.circle(self.frame, center, 5, (0, 0, 255), -1) # centroid'ini çizer
			else:
				center = (int(self.number_of_columns/2),int(self.number_of_lines/2))
				(self.center_x,self.center_y) = center
				yok_mu = 1	# contour yoksa pwm 0 vermesi için
				return yok_mu	
			#~ smallest_x = self.number_of_columns-1
			#~ smallest_y = self.number_of_lines-1
		else:
			center = (int(self.number_of_columns/2),int(self.number_of_lines/2))
			(self.center_x,self.center_y) = center
			yok_mu = 1	# contour yoksa pwm 0 vermesi için
			return yok_mu

		if self.center_x == 0:
			self.center_x += 1
		if self.center_y == 0:
			self.center_y += 1

		self.horizontal_pixels_of_balloon_ic = 2 * radius
		if radius > 0:
			print(self.horizontal_pixels_of_balloon_ic)
		else:
			print('YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOK!')
		# below are variables that are dependent on the camera.
		#~ try:
			#~ self.y_axis = (self.number_of_columns/2)*WIDTH_OF_BALLOON/self.horizontal_pixels_of_balloon	# real horizontal width/2 of the scene
			#~ self.z_axis = (self.number_of_lines/2)*WIDTH_OF_BALLOON/self.horizontal_pixels_of_balloon	# real vertical width/2 of the scene
		#~ except ZeroDivisionError:
			#~ yok_mu = 1	# contour yoksa pwm 0 vermesi için
			#~ return yok_mu
		# Above z_axis calculation was made due to the assumption that the balloon has circular shape.
		# i.e. its vertical width is equal to its horizontal width.
		return yok_mu
	def main(self):
		self.create_sliders()
		self.set_initials_of_sliders()
		#~ cap = PiCamera()		# uncomment etmek istersen import et
		#~ cap.resolution = (640, 480)
		#~ cap.framerate = 32
		#~ cap.vflip = True
		#~ rawCapture = PiRGBArray(cap, size=(640, 480)) # uncomment etmek istersen import et
		# allow the camera to warmup
		time.sleep(0.1)
		elapsedTime = 0.1 
		#~ for im_frame in cap.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		while True:
			resim = picam.read()
			#~ picam_picture = gor_class.Goruntu(resim,'balloon_config_file_picam.cnf',165,50,wrt_ground=45)
			#~ resim = im_frame.array
			bas = time.time()
			#~ ROOT.update()
			self.number_of_lines = resim.shape[0]
			self.number_of_columns = resim.shape[1]
			self.frame = cv2.GaussianBlur(resim, (5, 5), 0)
			hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
			
			HSVLOW, HSVHIGH= self.get_values_from_slider_positions()
			
			self.mask_ic = cv2.inRange(hsv, HSVLOW, HSVHIGH)
			kernel = np.ones((5,5), np.uint8) 
			# The first parameter is the original image, 
			# kernel is the matrix with which image is  
			# convolved and third parameter is the number  
			# of iterations, which will determine how much  
			# you want to erode/dilate a given image.  
			img_erosion = cv2.erode(self.mask_ic, kernel, iterations=3) 
			self.mask_ic = img_erosion
			#~ yeni = cv2.bitwise_and(self.frame,self.frame,mask=self.mask_ic)
			#~ gray = cv2.cvtColor(yeni, cv2.COLOR_BGR2GRAY)
			#~ self.th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
				#~ cv2.THRESH_BINARY,11,2)			
			self.find_center()
			# semi-otomatik angle ayarı:
			#~ try:
				#~ len_screen_vertical = self.number_of_lines / self.horizontal_pixels_of_balloon_ic * len_cisim
			#~ except:
				#~ print('YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOK!')
				#~ len_screen_vertical = 0
			#~ self.angle = np.arctan(len_screen_vertical / yatay_uzaklik)
			#~ picam_mask = picam_picture.build_mask()
			#~ kimse_yok_mu_picam = picam_picture.find_center(self.mask_ic)		
			#~ picam_picture.find_distance_to_center()
			#~ picam_picture.find_small_y_axis()
			#~ picam_picture.find_angle()
			#~ self.horizontal_pixels_of_balloon_ic = picam_picture.horizontal_pixels_of_balloon
			
			#~ deg_aci.set('angle:\t\t'+str(round(self.angle,2))+' degrees')
			#~ deg_sure.set('# Frames/second:\t'+str(round(1/elapsedTime,2))+' fps')
			
			mask_rescaled = self.rescale_frame(self.mask_ic, percent=per)
			#~ th3_rescaled = self.rescale_frame(self.th3, percent=per)
			frame_rescaled = self.rescale_frame(self.frame, percent=per)
			mask75_3_channel = cv2.cvtColor(mask_rescaled, cv2.COLOR_GRAY2BGR)
			# COLOR_GRAY2BGR ile gray'i renkli yapmıyo, 3 channel'lı yapıyo sadece concatanate yapabilmek için 
			ikisi= np.concatenate((mask75_3_channel,frame_rescaled), axis=0)
			cv2.imshow('Out_picam', ikisi)
			#~ cv2.imshow('th3_rescaled', th3_rescaled)
			#~ cv2.imshow('Mask', mask_rescaled)
			#~ cv2.imshow('Out', frame_rescaled)
			
			elapsedTime = time.time()-bas
			#~ rawCapture.truncate(0)
			if cv2.waitKey(5) & 0xFF == ord('q'): # check for q to quit program with 5ms delay
				break
		#~ cap.close()
		cv2.destroyAllWindows()
		picam.stop()
colorconfig = BalloonConfig()
colorconfig.main()
