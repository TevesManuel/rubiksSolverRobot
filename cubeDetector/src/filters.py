import cv2

from config import FILTER_MIN_BRIGHTNESS
from config import FILTER_ADD_BRIGHTNESS

def applyFilter(frame):
    frameWork = frame.copy()

    blackFrameMask = cv2.inRange(frameWork, (0, 0, 0), (FILTER_MIN_BRIGHTNESS, FILTER_MIN_BRIGHTNESS, FILTER_MIN_BRIGHTNESS))
    noBlackFrameMask = cv2.inRange(frameWork, (FILTER_MIN_BRIGHTNESS, FILTER_MIN_BRIGHTNESS, FILTER_MIN_BRIGHTNESS), (255, 255, 255))

    frameWork[blackFrameMask > 0] = (0, 0, 0)
    frameWork[noBlackFrameMask > 0] = cv2.add(frameWork[noBlackFrameMask > 0], (FILTER_ADD_BRIGHTNESS, FILTER_ADD_BRIGHTNESS, FILTER_ADD_BRIGHTNESS))

    grayScale = cv2.cvtColor(frameWork, cv2.COLOR_BGR2GRAY)

    smooth = cv2.GaussianBlur(grayScale, (5, 5), 1.5)

    edgesImage = cv2.Canny(smooth, 50, 100)

    return edgesImage