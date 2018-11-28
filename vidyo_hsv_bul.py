import cv2 as cv
import numpy as np
def rescale_frame(frame, percent=75):
	width = int(frame.shape[1] * percent/ 100)
	height = int(frame.shape[0] * percent/ 100)
	dim = (width, height)
	return cv.resize(frame, dim, interpolation = cv.INTER_AREA)
# optional argument for trackbars
def nothing(x):
    pass

# named ites for easy reference
barsWindow = 'Bars'
hl = 'H Low'
hh = 'H High'
sl = 'S Low'
sh = 'S High'
vl = 'V Low'
vh = 'V High'

# create window for the slidebars
cv.namedWindow(barsWindow, flags = cv.WINDOW_AUTOSIZE)

# create the sliders
cv.createTrackbar(hl, barsWindow, 0, 179, nothing)
cv.createTrackbar(hh, barsWindow, 0, 179, nothing)
cv.createTrackbar(sl, barsWindow, 0, 255, nothing)
cv.createTrackbar(sh, barsWindow, 0, 255, nothing)
cv.createTrackbar(vl, barsWindow, 0, 255, nothing)
cv.createTrackbar(vh, barsWindow, 0, 255, nothing)

# set initial values for sliders
cv.setTrackbarPos(hl, barsWindow, 0)
cv.setTrackbarPos(hh, barsWindow, 179)
cv.setTrackbarPos(sl, barsWindow, 0)
cv.setTrackbarPos(sh, barsWindow, 255)
cv.setTrackbarPos(vl, barsWindow, 0)
cv.setTrackbarPos(vh, barsWindow, 255)
while True:
	cap = cv.VideoCapture('uzun2.mp4')
	while True:
		ret, frame = cap.read()
		if ret == True:
			frame = cv.GaussianBlur(frame, (5, 5), 0)
			# print(cap.get(cv.CAP_PROP_POS_MSEC))
			# convert to HSV from BGR
			hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

			# read trackbar positions for all
			hul = cv.getTrackbarPos(hl, barsWindow)
			huh = cv.getTrackbarPos(hh, barsWindow)
			sal = cv.getTrackbarPos(sl, barsWindow)
			sah = cv.getTrackbarPos(sh, barsWindow)
			val = cv.getTrackbarPos(vl, barsWindow)
			vah = cv.getTrackbarPos(vh, barsWindow)

			# make array for final values
			HSVLOW = np.array([hul, sal, val])
			HSVHIGH = np.array([huh, sah, vah])

			# apply the range on a mask
			mask = cv.inRange(hsv, HSVLOW, HSVHIGH)
			maskedFrame = cv.bitwise_and(frame, frame, mask = mask)
			maskedFrame75 = rescale_frame(maskedFrame, percent=30)
			frame75 = rescale_frame(frame, percent=30)
			# display the camera and masked images
			cv.imshow('Masked', maskedFrame75)
			cv.imshow('Camera', frame75)

			# check for q to quit program with 5ms delay
			if cv.waitKey(5) & 0xFF == ord('q'):
				break
		else:
			break

	# clean up our resources
	cap.release()
	cv.destroyAllWindows()
