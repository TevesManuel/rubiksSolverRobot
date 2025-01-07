import cv2
import math

from config import CLUSTER_SIZE
from config import DETECTION_MAX_DISTANCE

def getFaceCube(squares):
    if len(squares) < CLUSTER_SIZE**2:
        return None

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

    centers = sorted(centers, key=lambda c: (c[1], c[0]))

    grid_centers = []
    for row in range(0, len(centers), CLUSTER_SIZE):
        grid = centers[row:row + CLUSTER_SIZE]
        if len(grid) < CLUSTER_SIZE:
            continue

        for i in range(len(grid) - 1):
            dist_x = abs(grid[i + 1][0] - grid[i][0])
            dist_y = abs(grid[i + 1][1] - grid[i][1])

            if dist_x > DETECTION_MAX_DISTANCE or dist_y > DETECTION_MAX_DISTANCE:
                return None

        grid_centers.extend(grid)

    if len(grid_centers) == CLUSTER_SIZE**2:
        return grid_centers
    return None


def findSquares(frame):
    contorns, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    squares = []

    for contorn in contorns:
        perimeter = cv2.arcLength(contorn, True)
        approach = cv2.approxPolyDP(contorn, 0.15 * perimeter, True)

        if len(approach) == 4:
            x, y, w, h = cv2.boundingRect(approach)
            aspectRatio = float(w) / h
            if 0.9 <= aspectRatio <= 1.1 and cv2.contourArea(approach) > 400:
                squares.append(approach)
    
    return squares