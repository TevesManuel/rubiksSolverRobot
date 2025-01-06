import cv2

from filters import applyFilter

from detection import findSquares
from detection import getFaceCube

from utils import closestColor

from solver import preprocessInput
from solver import cubeFaces

from config import WINDOW_TITLE

#Devs deps for debugging, etc
import time

facesRecognized = 0

lastFaceCubeLecture = []

if __name__ == '__main__':
    videoCapture = cv2.VideoCapture(0)

    while True:
        ret, frame = videoCapture.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        filteredFrame = applyFilter(frame)

        squares = findSquares(filteredFrame)

        newFaceCube = getFaceCube(squares)

        if newFaceCube != None:
            faceCubeColors = []
            for center in newFaceCube:
                faceCubeColors.append(closestColor(frame[center[1], center[0]]))
            
            k = faceCubeColors[2]
            faceCubeColors[2] = faceCubeColors[0]
            faceCubeColors[0] = k
            k = faceCubeColors[5]
            faceCubeColors[5] = faceCubeColors[3]
            faceCubeColors[3] = k
            k = faceCubeColors[8]
            faceCubeColors[8] = faceCubeColors[6]
            faceCubeColors[6] = k

            if cubeFaces[faceCubeColors[4]+"Face"] == []:
                cubeFaces[faceCubeColors[4]+"Face"] = faceCubeColors
                facesRecognized += 1
                print("Face " + faceCubeColors[4] + " is already registered.")
                print("Faces: " + str(facesRecognized) + "/6")
            
            lastFaceCubeLecture = newFaceCube


            if facesRecognized == 6:
                preprocessedInput = preprocessInput(cubeFaces)
                print("Preprocessed input is ", preprocessedInput)
                print("Has ", preprocessedInput.count('U'), "/9 U.")
                print("Has ", preprocessedInput.count('R'), "/9 R.")
                print("Has ", preprocessedInput.count('F'), "/9 F.")
                print("Has ", preprocessedInput.count('D'), "/9 D.")
                print("Has ", preprocessedInput.count('L'), "/9 L.")
                print("Has ", preprocessedInput.count('B'), "/9 B.")
    
        cv2.drawContours(frame, squares, -1, (0, 255, 0), 10)

        if len(lastFaceCubeLecture) > 0:
            for center in lastFaceCubeLecture:
                cv2.circle(frame, center, radius=10, color=(255, 0, 0), thickness=-1)

        cv2.imshow(WINDOW_TITLE, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    videoCapture.release()
    cv2.destroyAllWindows()