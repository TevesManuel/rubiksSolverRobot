import cv2
import math

from config import DETECTION_CLUSTER_SIZE
from config import DETECTION_MIN_DISTANCE_BETWEEN_CENTERS
from config import DETECTION_MIN_AREA

def getFaceCube(squares):
    centers = []
    for square in squares:
        M = cv2.moments(square)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            newCenter = (cx, cy)
            
            enabled = True
            for existingCenter in centers:
                dist = math.sqrt((existingCenter[0] - cx) ** 2 + (existingCenter[1] - cy) ** 2)
                if dist <= 2:
                    enabled = False
                    break

            if enabled:
                centers.append(newCenter)

    cube_x_axis = []
    cube_y_axis = []

    for center in centers:
        y = center[0]
        
        belongs = False
        for i in range(len(cube_y_axis)):
            if abs(cube_y_axis[i] - y) <= DETECTION_MIN_DISTANCE_BETWEEN_CENTERS:
                belongs = True
                break
        if not belongs:
            cube_y_axis.append(y)

        x = center[1]

        belongs = False
        for i in range(len(cube_x_axis)):
            if abs(cube_x_axis[i] - x) <= DETECTION_MIN_DISTANCE_BETWEEN_CENTERS:
                belongs = True
                break
        if not belongs:
            cube_x_axis.append(x)
    
    cube_x_axis.sort()
    cube_y_axis.sort()

    faceCube = None

    if len(cube_x_axis) == len(cube_y_axis) == DETECTION_CLUSTER_SIZE:
        faceCube = []
    
        for x in cube_x_axis:
            for y in cube_y_axis:
                faceCube.append((y, x))

    return faceCube


def findSquares(frame):
    contorns, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    squares = []

    for contorn in contorns:
        perimeter = cv2.arcLength(contorn, True)
        approach = cv2.approxPolyDP(contorn, 0.15 * perimeter, True)

        if len(approach) == 4:
            x, y, w, h = cv2.boundingRect(approach)
            aspectRatio = float(w) / h
            if 0.9 <= aspectRatio <= 1.1 and cv2.contourArea(approach) > DETECTION_MIN_AREA:
                squares.append(approach)
    
    return squares