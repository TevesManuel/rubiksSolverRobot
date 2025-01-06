import cv2
from config import WINDOW_TITLE
from config import FILTER_MIN_BRIGHTNESS
from config import FILTER_ADD_BRIGHTNESS
from config import CLUSTER_SIZE
from config import DETECTION_MAX_DISTANCE

#Devs deps for debugging, etc
import time

def areSquaresClustered(squares):
    if len(squares) < CLUSTER_SIZE**2:
        return False

    centers = []
    for square in squares:
        M = cv2.moments(square)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centers.append((cx, cy))

    centers = sorted(centers, key=lambda c: (c[1], c[0]))

    for row in range(0, len(centers), CLUSTER_SIZE):
        grid = centers[row:row + CLUSTER_SIZE]
        if len(grid) < CLUSTER_SIZE:
            continue

        for i in range(len(grid) - 1):
            dist_x = abs(grid[i + 1][0] - grid[i][0])
            dist_y = abs(grid[i + 1][1] - grid[i][1])

            if dist_x > DETECTION_MAX_DISTANCE or dist_y > DETECTION_MAX_DISTANCE:
                return False

    return True

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

def findSquares(frame):
    contorns, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    squares = []

    for contorn in contorns:
        perimeter = cv2.arcLength(contorn, True)
        approach = cv2.approxPolyDP(contorn, 0.04 * perimeter, True)

        if len(approach) == 4 and cv2.isContourConvex(approach):
            x, y, w, h = cv2.boundingRect(approach)
            aspectRatio = float(w) / h
            if 0.9 <= aspectRatio <= 1.1 and w * h > 100:
                squares.append(approach)
    
    return squares

if __name__ == '__main__':
    videoCapture = cv2.VideoCapture(0)

    while True:
        ret, frame = videoCapture.read()
        if not ret:
            break

        filteredFrame = applyFilter(frame)

        squares = findSquares(filteredFrame)

        if areSquaresClustered(squares):
            print("Cube detected:", time.time())
        
        cv2.drawContours(frame, squares, -1, (0, 255, 0), 10)

        cv2.imshow(WINDOW_TITLE, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    videoCapture.release()
    cv2.destroyAllWindows()