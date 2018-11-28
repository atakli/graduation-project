import numpy as np
import cv2
per=15
def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
frame = cv2.imread('r1.jpg')
blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

lower_blue = np.array([68, 82, 94])
upper_blue = np.array([82, 255, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)

_, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

for contour in contours:
	area = cv2.contourArea(contour)

	if area > 5000:
		cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)
		
frame75 = rescale_frame(frame, percent=per)
# mask75 = rescale_frame(mask, percent=per)

cv2.imshow("Frame", frame75)
# cv2.imshow("Mask", mask75)

cv2.waitKey()