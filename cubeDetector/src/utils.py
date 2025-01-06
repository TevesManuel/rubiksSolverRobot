import numpy as np

REFERENCE_COLORS = {
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "orange": (0, 165, 255),
    "yellow": (0, 255, 255),
    "white": (255, 255, 255)
}

def closestColor(color):
    minDist = float('inf')
    closestColorName = ""

    for colorName, refColor in REFERENCE_COLORS.items():
        dist = np.linalg.norm(np.array(color) - np.array(refColor))

        if dist < minDist:
            minDist = dist
            closestColorName = colorName

    return closestColorName