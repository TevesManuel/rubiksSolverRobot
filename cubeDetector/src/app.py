import cv2
import numpy as np

from filters import applyFilter

from detection import findSquares
from detection import getFaceCube

from utils import closestColor

from solver import preprocessInput
from solver import cubeFaces
from solver import isValidInput
from solver import debugPreprocessedInput
from solver import solve
from solver import countCubeColors

from config import WINDOW_TITLE

class App:
    def __init__(self):
        self.videoCapture = cv2.VideoCapture(0)

        self.facesRecognized = 0
        self.lastFaceCubeLecture = []
        self.isAllCubeReaded = False

    def getColors(self, newFaceCube, frame):
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

        return faceCubeColors

    def detectionView(self):
        ret, frame = self.videoCapture.read()
        if not ret:
            return True

        frame = cv2.flip(frame, 1)

        filteredFrame = applyFilter(frame)

        if not self.isAllCubeReaded:

            squares = findSquares(filteredFrame)
            newFaceCube = getFaceCube(squares)

            if newFaceCube != None:
                faceCubeColors = self.getColors(newFaceCube, frame)

                if cubeFaces[faceCubeColors[4]+"Face"] == []:
                    cubeFaces[faceCubeColors[4]+"Face"] = faceCubeColors
                    self.facesRecognized += 1
                    print("Face " + faceCubeColors[4] + " is already registered.")
                    print("Faces: " + str(self.facesRecognized) + "/6")
                    print("\n", faceCubeColors, "\n")   

                self.lastFaceCubeLecture = newFaceCube

                if self.facesRecognized == 6:
                    self.videoCapture.release()
                    self.isAllCubeReaded = True
                    preprocessedInput = preprocessInput(cubeFaces)
                    print("Preprocessed input is ", preprocessedInput)
                    if isValidInput(preprocessedInput):
                        print("The input is valid.")
                        solution = solve(preprocessedInput)
                        print("The solution is ", solution)
                    else:
                        debugPreprocessedInput(preprocessedInput)
                        
                # Graphic debug
                cv2.drawContours(frame, squares, -1, (0, 255, 0), 10)

                if len(self.lastFaceCubeLecture) > 0:
                    for center in self.lastFaceCubeLecture:
                        cv2.circle(frame, center, radius=10, color=(255, 0, 0), thickness=-1)

        # Render

        cv2.imshow(WINDOW_TITLE, frame)

        # Controls

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return True

    def close(self):
        self.videoCapture.release()
        cv2.destroyAllWindows()    

    def run(self):

        camera_dimensions = (int(self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), 3)

        while True:
            if not self.isAllCubeReaded:
                if self.detectionView():
                    break
            else:
                frame = np.zeros(camera_dimensions, dtype=np.uint8)

                cubeColors = countCubeColors(preprocessInput(cubeFaces))

                cv2.putText(frame, "White is "  + str(cubeColors["white"])  + "/9", (10, 20 + 0*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255) if cubeColors["white"]  != 9 else (255, 255, 255), 1)
                cv2.putText(frame, "Blue is "   + str(cubeColors["blue"])   + "/9", (10, 20 + 1*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255) if cubeColors["blue"]   != 9 else (255, 255, 255), 1)
                cv2.putText(frame, "Red is "    + str(cubeColors["red"])    + "/9", (10, 20 + 2*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255) if cubeColors["red"]    != 9 else (255, 255, 255), 1)
                cv2.putText(frame, "Yellow is " + str(cubeColors["yellow"]) + "/9", (10, 20 + 3*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255) if cubeColors["yellow"] != 9 else (255, 255, 255), 1)
                cv2.putText(frame, "Green is "  + str(cubeColors["green"])  + "/9", (10, 20 + 4*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255) if cubeColors["green"]  != 9 else (255, 255, 255), 1)
                cv2.putText(frame, "Orange is " + str(cubeColors["orange"]) + "/9", (10, 20 + 5*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255) if cubeColors["orange"] != 9 else (255, 255, 255), 1)

                cv2.imshow(WINDOW_TITLE, frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                if cv2.waitKey(1) & 0xFF == ord(' '):
                    print("Solve")
        self.close()
            

                