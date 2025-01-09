import cv2

class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.clickDown = False
        self.clickUp   = False
        self.click     = False
        self.payload = "white"

    def handleClick(self, event, x, y, flags, param):
        self.x = x
        self.y = y
        if event == cv2.EVENT_LBUTTONDOWN:
            self.clickDown = True
        if event == cv2.EVENT_LBUTTONUP:
            self.clickUp = True
    
    def setup(self, windowName):
        cv2.setMouseCallback(windowName, self.handleClick)
    
    def update(self):
        if self.clickDown and not self.click:
            self.click = True
        elif self.clickDown and self.click:
            self.clickDown = False
        if self.clickUp and self.click:
            self.click = False
        elif self.clickUp and not self.click:
            self.clickUp = False

    def debug(self):
        print("X: ", self.x)
        print("Y: ", self.y)
        print("MLB DOWN: ", self.clickDown)
        print("MLB: ", self.click)
        print("MLB Up: ", self.clickUp)