import numpy as np
import cv2

COLOR_RANGES_HSV = {
    "red": [(0, 50, 50), (10, 255, 255)],
    "red2": [(170, 50, 50), (180, 255, 255)],
    "green": [(35, 50, 50), (85, 255, 255)],
    "blue": [(90, 50, 50), (130, 255, 255)],
    "orange": [(10, 100, 100), (20, 255, 255)],
    "yellow": [(20, 100, 100), (30, 255, 255)],
    "white": [(0, 0, 200), (180, 50, 255)]
}

def hsvClassifier(colorBGR):
    colorHsv = cv2.cvtColor(np.uint8([[colorBGR]]), cv2.COLOR_BGR2HSV)[0][0]

    for colorName, (lower, upper) in COLOR_RANGES_HSV.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        if cv2.inRange(np.uint8([[colorHsv]]), lower, upper).any():
            return colorName.replace("2", "")

    return "unknown"

REFERENCE_COLORS = {
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "orange": (0, 165, 255),
    "yellow": (0, 255, 255),
    "white": (255, 255, 255)
}

def rgbClassifier(color):
    minDist = float('inf')
    closestColorName = ""

    for colorName, refColor in REFERENCE_COLORS.items():
        dist = np.linalg.norm(np.array(color) - np.array(refColor))

        if dist < minDist:
            minDist = dist
            closestColorName = colorName

    return closestColorName

def closestColor(color):
    rgbResult = rgbClassifier(color)
    if rgbResult == 'orange' or rgbResult == 'yellow':
        return rgbResult
    hsvResult = hsvClassifier(color)
    if hsvResult != "unknown":
        return hsvResult
    return rgbResult