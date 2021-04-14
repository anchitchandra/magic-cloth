import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


def make_720p():
    cap.set(3, 1920)
    cap.set(4, 1080)


make_720p()
time.sleep(3)
for i in range(30):
    frame, background = cap.read()
background = np.flip(background, axis=1)

while True:
    frame, res = cap.read()
    if not frame:
        break
    res = np.flip(res, axis=1)
    hsv = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 120, 50])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    mask1 = mask1 + mask2
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    mask2 = cv2.bitwise_not(mask1)
    res1 = cv2.bitwise_and(res, res, mask=mask2)
    res2 = cv2.bitwise_and(background, background, mask=mask1)
    final = cv2.addWeighted(res1, 1, res2, 1, 0)
    cv2.imshow("harrypotter", final)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
