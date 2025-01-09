import cv2
import numpy as np

from mouse import Mouse
from filters import applyFilter

from detection import findSquares
from detection import getFaceCube

from utils import closestColor
from utils import drawCube
from utils import drawControls
from utils import drawCubeStats
from utils import drawButtonsControls
from utils import ControlsReturnValue

from solver import preprocessInput
from solver import cubeFaces
from solver import isValidInput
from solver import debugPreprocessedInput
from solver import solve
from solver import resetCubeFaces

from config import WINDOW_TITLE
from config import WINDOW_SIZE

class App:
    def __init__(self):
        self.videoCapture = cv2.VideoCapture(0)

        self.mouse = Mouse()

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
                        print("The input is invalid.")
                        
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

        camera_dimensions = (WINDOW_SIZE, WINDOW_SIZE, 3)

        cv2.namedWindow(WINDOW_TITLE)
        
        self.mouse.setup(WINDOW_TITLE)

        while True:
            
            self.mouse.update()
            # self.mouse.debug()

            if not self.isAllCubeReaded:
                if self.detectionView():
                    break
            else:
                frame = np.zeros(camera_dimensions, dtype=np.uint8)

                drawCubeStats(frame)

                drawCube(frame, cubeFaces, (40, 220), self.mouse)
                drawControls(frame, (20, 500), self.mouse)
                newInstruction = drawButtonsControls(frame, (450, 20), self.mouse)

                cv2.imshow(WINDOW_TITLE, frame)
                
                if newInstruction == ControlsReturnValue.REBOOT:
                    self.isAllCubeReaded = False
                    self.lastFaceCubeLecture = []
                    self.facesRecognized = 0
                    self.videoCapture = cv2.VideoCapture(0)
                    resetCubeFaces()

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                if (cv2.waitKey(1) & 0xFF == ord(' ')) or newInstruction == ControlsReturnValue.SOLVE:
                    preprocessedInput = preprocessInput(cubeFaces)
                    print("Preprocessed input is ", preprocessedInput)
                    if isValidInput(preprocessedInput):
                        print("The input is valid.")
                        solution = solve(preprocessedInput)
                        print("The solution is ", solution)
                    else:
                        print("The input is invalid.")
        self.close()
            

                