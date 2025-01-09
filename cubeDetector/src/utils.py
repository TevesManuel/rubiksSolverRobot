from mimetypes import init
import numpy as np
import cv2

from config import GRAPHICS_OFFSET_CUBEFACE
from config import GRAPHICS_SIZE_CUBEFACE

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

def stringToBGR(color):
    if color == "red":
        return (0, 0, 255)
    if color == "green":
        return (0, 255, 0)
    if color == "blue":
        return (255, 0, 0)
    if color == "orange": 
        return(0, 165, 255)
    if color == "yellow":
        return(0, 255, 255)
    if color == "white":
        return (255, 255, 255)

from solver import cubeFaces
from solver import preprocessInput

def countCubeColors(preprocessedInput):
    return {
        "white"  : preprocessedInput.count('U'),
        "blue"   : preprocessedInput.count('R'),
        "red"    : preprocessedInput.count('F'),
        "yellow" : preprocessedInput.count('D'),
        "green"  : preprocessedInput.count('L'),
        "orange" : preprocessedInput.count('B'),
    }


def drawCubeStats(frame):
    cubeColors = countCubeColors(preprocessInput(cubeFaces))

    cv2.putText(frame, "White is "  + str(cubeColors["white"])  + "/9", (10, 20 + 0*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255) if cubeColors["white"]  != 9 else (255, 255, 255), 1)
    cv2.putText(frame, "Blue is "   + str(cubeColors["blue"])   + "/9", (10, 20 + 1*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255) if cubeColors["blue"]   != 9 else (255, 255, 255), 1)
    cv2.putText(frame, "Red is "    + str(cubeColors["red"])    + "/9", (10, 20 + 2*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255) if cubeColors["red"]    != 9 else (255, 255, 255), 1)
    cv2.putText(frame, "Yellow is " + str(cubeColors["yellow"]) + "/9", (10, 20 + 3*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255) if cubeColors["yellow"] != 9 else (255, 255, 255), 1)
    cv2.putText(frame, "Green is "  + str(cubeColors["green"])  + "/9", (10, 20 + 4*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255) if cubeColors["green"]  != 9 else (255, 255, 255), 1)
    cv2.putText(frame, "Orange is " + str(cubeColors["orange"]) + "/9", (10, 20 + 5*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255) if cubeColors["orange"] != 9 else (255, 255, 255), 1)

def drawCubeFace(frame, initialPosition, cubeFaceColors, mouse):
    for i in range(9):
        x = initialPosition[0] + (i%3)*(GRAPHICS_OFFSET_CUBEFACE + GRAPHICS_SIZE_CUBEFACE)
        y = initialPosition[1] + int(i/3)*(GRAPHICS_OFFSET_CUBEFACE + GRAPHICS_SIZE_CUBEFACE)                    
        if mouse.clickDown and mouse.x > x and mouse.x < x + GRAPHICS_SIZE_CUBEFACE and mouse.y > y and mouse.y < y + GRAPHICS_SIZE_CUBEFACE:
            cubeFaceColors[i] = mouse.payload
        cv2.rectangle(frame,(x, y), (x + GRAPHICS_SIZE_CUBEFACE, y + GRAPHICS_SIZE_CUBEFACE), stringToBGR(cubeFaceColors[i]), -1)
    return (3*GRAPHICS_SIZE_CUBEFACE + 2*GRAPHICS_OFFSET_CUBEFACE, 3*GRAPHICS_SIZE_CUBEFACE + 2*GRAPHICS_OFFSET_CUBEFACE)

def drawCube(frame, cubeFaces, initialPosition, mouse):
    offset = 2*GRAPHICS_OFFSET_CUBEFACE
    dim = drawCubeFace(frame, initialPosition, cubeFaces['orangeFace'], mouse)
    new_x_pos = dim[0] + initialPosition[0] + offset
    drawCubeFace(frame, (new_x_pos, initialPosition[1]), cubeFaces['greenFace'], mouse)
    new_x_pos = new_x_pos + dim[0] + offset
    redPosition = (new_x_pos, initialPosition[1])
    drawCubeFace(frame, redPosition, cubeFaces['redFace'], mouse)
    drawCubeFace(frame, (redPosition[0], redPosition[1] - dim[1] - offset), cubeFaces['whiteFace'], mouse)
    drawCubeFace(frame, (redPosition[0], redPosition[1] + dim[1] + offset), cubeFaces['yellowFace'], mouse)
    drawCubeFace(frame, (redPosition[0] + dim[0] + offset, redPosition[1]), cubeFaces['blueFace'], mouse)

def drawControls(frame, initialPosition, mouse):
    cv2.putText(frame, "Click on the colors below to select them, then correct the cube above.", initialPosition, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, "When you're done, press space to solve.", (initialPosition[0], initialPosition[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    for i, color in enumerate(REFERENCE_COLORS.keys()):
        a = 2*(GRAPHICS_OFFSET_CUBEFACE + GRAPHICS_SIZE_CUBEFACE)
        b = 2 * GRAPHICS_SIZE_CUBEFACE
        x = initialPosition[0] + i*a
        y = initialPosition[1] + 60
        cv2.rectangle(frame,(x, y), (x + b, y + b), stringToBGR(color), -1)
        if mouse.clickDown and mouse.x > x and mouse.x < x + b and mouse.y > y and mouse.y < y + b:
            mouse.payload = color