import numpy as np
import cv2

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

cap = cv2.VideoCapture('uzun4.mp4')

while True:
    _, frame = cap.read()
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([61, 77, 0])
    upper_blue = np.array([255, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 5000:
            cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)

    frame75 = rescale_frame(frame, percent=30)
    mask75 = rescale_frame(mask, percent=30)

    cv2.imshow("Frame", frame75)
    cv2.imshow("Mask", mask75)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()