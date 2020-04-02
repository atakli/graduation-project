#                      __    __    __    __
#                     /  \  /  \  /  \  /  \ 
#____________________/  __\/  __\/  __\/  __\_____________________________
#___________________/  /__/  /__/  /__/  /________________________________
#                   | / \   / \   / \   / \   \___
#                   |/   \_/   \_/   \_/   \    o \ 
#                                           \_____/--<
import cv2
import numpy as np
#~ import time
#~ import random
import imutils
# gor_class'ı import ederken 0.98 saniye geçti, yani heralde sadece cv2,numpy ve time modülleri için
# Thing to remember is, always try to avoid loops and iterations in Python. 
# Instead, use array manipulation facilities available in Numpy (and OpenCV).
# Simply adding two numpy arrays using C = A+B is a lot times faster than using double loops.
pi = np.pi
# fov_angle_horizontal = 53.50 #np.arctan(self.y_axis/KNOWN_DISTANCE)*180/pi*2 # not sure this calculation is true
# fov_angle_vertical = 41.41 #np.arctan(self.z_axis/KNOWN_DISTANCE)*180/pi*2 # not sure this calculation is true
# Actually, we don't need calculation for fov angles. they are already constant.
WIDTH_OF_BALLOON = 22
#~ try:
	#~ from picamera.array import PiRGBArray as PiRGBArray
	#~ from picamera import PiCamera as PiCamera
#~ except ImportError:
	#~ print("picamera not installed - please install if running on RPI")

class Goruntu:
	def __init__(self,resim,configuration_dosyasi,known_pix,known_dis,wrt_ground):
		# __init__ içinde de fonksiyon çağırabilirim. (self.personele_ekle gibi) belki lazım olur
		self.resim = resim
		self.resim = cv2.GaussianBlur(self.resim, (5, 5), 0)
		self.number_of_lines = self.resim.shape[0]		# bunları da çıkarıcam. Yani bi kereden sonra hesaplanmasın
		self.number_of_columns = self.resim.shape[1]	
		self.KNOWN_PIXEL =  known_pix #187	# known horizontal_pixels_of_balloon at a known distance # netbook kamerasının eski değerleri
		self.KNOWN_DISTANCE =  known_dis #85	# it is a known distance where the sample picture is taken
		self.camera_angle_wrt_ground = wrt_ground
		self.conf = configuration_dosyasi
		with open(configuration_dosyasi) as dosya:
			veri = dosya.readlines()
		self.HSVLOW = np.array([int(veri[0][8:-1]), int(veri[2][8:-1]), int(veri[4][8:-1])])
		self.HSVHIGH = np.array([int(veri[1][9:-1]), int(veri[3][9:-1]), int(veri[5][9:-1])])
	def rescale_frame(self,resim_to_be_rescaled, percent=75):
		width = int(resim_to_be_rescaled.shape[1] * percent/ 100)
		height = int(resim_to_be_rescaled.shape[0] * percent/ 100)
		dim = (width, height)
		return cv2.resize(resim_to_be_rescaled, dim, interpolation = cv2.INTER_AREA)
	def build_mask(self):
		#~ self.blur_falan()									# bu fonksiyonda bu ve
		self.hsv = cv2.cvtColor(self.resim, cv2.COLOR_BGR2HSV)	# bu satır zaman teşkil ediyo gibi
		self.mask = cv2.inRange(self.hsv, self.HSVLOW, self.HSVHIGH)
		
		kernel = np.ones((6,6), np.uint8) 
		# The first parameter is the original image, 
		# kernel is the matrix with which image is  
		# convolved and third parameter is the number  
		# of iterations, which will determine how much  
		# you want to erode/dilate a given image.  
		img_erosion = cv2.erode(self.mask, kernel, iterations=3) # 1.7 msec civarında
		
		self.mask = img_erosion
		# self.th2 = cv2.adaptiveThreshold(self.resim,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
		# cv2.THRESH_BINARY,11,2)
		#~ self.th3 = cv2.adaptiveThreshold(self.mask,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
				#~ cv2.THRESH_BINARY,11,2)
		# self.resim = cv2.Canny(self.resim,50,60)
		#~ img_dilation = cv2.dilate(self.mask, kernel, iterations=1) 
		
		# hsv'yi bi deney için self'li yaptım. geri alınabilir. ama zararı da yok gibi.
		return self.mask
	def find_center(self,mas):
		# bas = time.time()
		#~ _, contours, _ = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
		cnts = cv2.findContours(mas.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
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
			#~ cv2.ellipse(self.resim,ellipse,(0,255,0),2)	# denenebilir
			
			M = cv2.moments(c)

			try:
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			except ZeroDivisionError:
				center = (0,0)
			(self.center_x,self.center_y) = center
			# only proceed if the radius meets a minimum size
			if radius > 25: # eğer balonun radius'u 10'dan büyükse algıla, yoksa algılama çünkü o şey balon olmayabilir
				cv2.circle(self.resim, (int(x), int(y)), int(radius), (0, 255, 255), 2) # balonun çevresini çizer
				cv2.circle(self.resim, center, 5, (0, 0, 255), -1) # centroid'ini çizer
			else:
				center = (int(self.number_of_columns/2),int(self.number_of_lines/2))
				(self.center_x,self.center_y) = center
				yok_mu = 1	# contour yoksa pwm 0 vermesi için
				return yok_mu	
			smallest_x = self.number_of_columns-1
			smallest_y = self.number_of_lines-1
		else:
			center = (int(self.number_of_columns/2),int(self.number_of_lines/2))
			(self.center_x,self.center_y) = center
			yok_mu = 1	# contour yoksa pwm 0 vermesi için
			return yok_mu

		if self.center_x == 0:
			self.center_x += 1
		if self.center_y == 0:
			self.center_y += 1

		self.horizontal_pixels_of_balloon = 2 * radius
		
		# below are variables that are dependent on the camera.
		try:
			self.y_axis = (self.number_of_columns/2)*WIDTH_OF_BALLOON/self.horizontal_pixels_of_balloon	# real horizontal width/2 of the scene
			# bu aslında ekranın kenarı ve ortasında farklı olmalı ama çok değişmiyo heralde
			self.z_axis = (self.number_of_lines/2)*WIDTH_OF_BALLOON/self.horizontal_pixels_of_balloon	# real vertical width/2 of the scene
		except ZeroDivisionError:
			yok_mu = 1	# contour yoksa pwm 0 vermesi için
			return yok_mu
		return yok_mu
	def find_small_y_axis(self,fov_horizontal):
		if self.center_x < self.number_of_columns / 2:
			ratio = (self.number_of_columns / 2 - self.center_x ) / (self.center_x)								# a / b
			self.small_y_axis = - self.y_axis * ratio / (ratio + 1)				# closer portion to the center of the image
			self.angle = - fov_horizontal / 2 * ratio / (ratio + 1) * pi/180
		elif self.center_x > self.number_of_columns / 2:
			ratio = (self.center_x - self.number_of_columns / 2) / (self.number_of_columns - self.center_x)		# a / b
			self.small_y_axis = self.y_axis * ratio / (ratio + 1)				# closer portion to the center of the image
			self.angle = fov_horizontal / 2 * ratio / (ratio + 1) * pi/180
		else:
			self.small_y_axis = 0
			self.angle = 0
	def find_vertical_angle(self,fov_vertical):
		if self.center_y < self.number_of_lines / 2:
			ratio = (self.number_of_lines / 2 - self.center_y ) / (self.center_y)							# a / b
			self.ver_ang = fov_vertical / 2 * ratio / (ratio + 1)
			#~ self.small_z_axis = self.z_axis * ratio / (ratio + 1)				# closer portion to the center of the image
		elif self.center_y > self.number_of_lines / 2:
			ratio = (self.center_y - self.number_of_lines / 2) / (self.number_of_lines - self.center_y)		# a / b
			self.ver_ang = - fov_vertical / 2 * ratio / (ratio + 1)
			#~ self.small_z_axis = self.z_axis * ratio / (ratio + 1)				# closer portion to the center of the image
		else:
			#~ self.small_z_axis = 0
			self.ver_ang = 0
	def find_distance_to_center(self):
		try:
			self.distance_to_center = (self.KNOWN_PIXEL * self.KNOWN_DISTANCE) / self.horizontal_pixels_of_balloon
		except:
			self.distance_to_center = 300
		# self.height_of_image_center = self.distance_to_center * np.sin(self.camera_angle_wrt_ground*pi/180)
		self.projection_of_distance_to_center =  self.distance_to_center*np.cos((self.camera_angle_wrt_ground+self.ver_ang)*pi/180)
		self.projection_of_distance_to_actual_place_of_balloon = pow( pow(self.projection_of_distance_to_center,2) + pow(self.small_y_axis,2) ,1/2)
