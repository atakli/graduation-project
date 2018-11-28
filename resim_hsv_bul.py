import cv2 as cv
import numpy as np
per = 15
# optional argument for trackbars
def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv.resize(frame, dim, interpolation = cv.INTER_AREA)
def nothing(x):
    pass
resim = cv.imread('r1.jpg')
number_of_lines = resim.shape[0]
number_of_columns = resim.shape[1]


# named ites for easy reference
barsWindow = 'Bars'
bar_area = 'Area Bar'
hl = 'H Low'
hh = 'H High'
sl = 'S Low'
sh = 'S High'
vl = 'V Low'
vh = 'V High'
area_bar = 'Area'
# create window for the slidebars
cv.namedWindow(barsWindow, flags = cv.WINDOW_AUTOSIZE)
cv.namedWindow(bar_area, flags = cv.WINDOW_AUTOSIZE)
cv.resizeWindow(barsWindow, 500,315)
cv.resizeWindow(bar_area, 500,50)

# create the sliders
cv.createTrackbar(hl, barsWindow, 0, 179, nothing)
cv.createTrackbar(hh, barsWindow, 0, 179, nothing)
cv.createTrackbar(sl, barsWindow, 0, 255, nothing)
cv.createTrackbar(sh, barsWindow, 0, 255, nothing)
cv.createTrackbar(vl, barsWindow, 0, 255, nothing)
cv.createTrackbar(vh, barsWindow, 0, 255, nothing)
cv.createTrackbar(vh, barsWindow, 0, 255, nothing)
cv.createTrackbar(area_bar, bar_area, 0, 200000, nothing)

# set initial values for sliders
cv.setTrackbarPos(hl, barsWindow, 68)
cv.setTrackbarPos(hh, barsWindow, 82)
cv.setTrackbarPos(sl, barsWindow, 82)
cv.setTrackbarPos(sh, barsWindow, 255)
cv.setTrackbarPos(vl, barsWindow, 94)
cv.setTrackbarPos(vh, barsWindow, 255)
cv.setTrackbarPos(area_bar, bar_area, 165000)

while(True):
	frame = cv.GaussianBlur(resim, (5, 5), 0)
	hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
	# read trackbar positions for all
	hul = cv.getTrackbarPos(hl, barsWindow)
	huh = cv.getTrackbarPos(hh, barsWindow)
	sal = cv.getTrackbarPos(sl, barsWindow)
	sah = cv.getTrackbarPos(sh, barsWindow)
	val = cv.getTrackbarPos(vl, barsWindow)
	vah = cv.getTrackbarPos(vh, barsWindow)
	area_bared = cv.getTrackbarPos(area_bar, bar_area)

	# make array for final values
	HSVLOW = np.array([hul, sal, val])
	HSVHIGH = np.array([huh, sah, vah])

	# apply the range on a mask
	mask = cv.inRange(hsv, HSVLOW, HSVHIGH)
	
	_, contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
	a=0
	for contour in contours:
		area = cv.contourArea(contour)
		biggest_x = 0
		biggest_y = 0
		smallest_x = number_of_columns-1
		smallest_y = number_of_lines-1
		if area > area_bared:
			cv.drawContours(frame, contour, -1, (0, 255, 0), 6)
			a=a+1
			for i in range(len(contour)):
				if contour[i][0][0] > biggest_x:
					biggest_x = contour[i][0][0]
				if contour[i][0][0] < smallest_x:
					smallest_x = contour[i][0][0]
				if contour[i][0][1] > biggest_y:
					biggest_y = contour[i][0][1]
				if contour[i][0][1] < smallest_y:
					smallest_y = contour[i][0][1]
			break
	center_x = int(round((smallest_x+biggest_x)/2))		
	center_y = int(round((smallest_y+biggest_y)/2))
	# print('# of contours: ',a)
	# maskedFrame = cv.bitwise_and(frame, frame, mask = mask)
	# maskedFrame75 = rescale_frame(maskedFrame, percent=per)
	cv.circle(frame, (center_x,center_y), 50, (0,0,0), 10)
	frame75 = rescale_frame(frame, percent=per)

	# cv.imshow('Masked', maskedFrame75)
	cv.imshow('Out', frame75)
	# check for q to quit program with 5ms delay
	if cv.waitKey(5) & 0xFF == ord('q'):
		break
def center(center_x,center_y):
	return (center_x,center_y)