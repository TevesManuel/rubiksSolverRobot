import cv2

from filters import applyFilter

from detection import findSquares
from detection import getFaceCube

from utils import closestColor

from config import WINDOW_TITLE

#Devs deps for debugging, etc
import time


faceCube = []
faceCubeColors = []

if __name__ == '__main__':
    videoCapture = cv2.VideoCapture(0)

    while True:
        ret, frame = videoCapture.read()
        if not ret:
            break

        filteredFrame = applyFilter(frame)

        squares = findSquares(filteredFrame)

        newFaceCube = getFaceCube(squares)

        if newFaceCube != None:
            print("Cube detected:", time.time())
            print(newFaceCube)
            faceCubeColors = []
            for center in newFaceCube:
                faceCubeColors.append(frame[center[1], center[0]])
            for color in faceCubeColors:
                print(color)
                print(closestColor(color))
            faceCube = newFaceCube
    
        cv2.drawContours(frame, squares, -1, (0, 255, 0), 10)

        if len(faceCube) > 0:
            for center in faceCube:
                cv2.circle(frame, center, radius=10, color=(255, 0, 0), thickness=-1)

        cv2.imshow(WINDOW_TITLE, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    videoCapture.release()
    cv2.destroyAllWindows()