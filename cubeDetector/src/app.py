import cv2
from config import WINDOW_TITLE

def findSquares(frame):
    contorns, _ = cv2.findContours(edgesImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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

MIN = 100
SUM = 255

if __name__ == '__main__':
    videoCapture = cv2.VideoCapture(0)

    while True:
        ret, frame = videoCapture.read()
        if not ret:
            break

        noBlackFrame = cv2.inRange(frame, (MIN, MIN, MIN), (255, 255, 255))
        frame[noBlackFrame > 0] = cv2.add(frame[noBlackFrame > 0], (SUM, SUM, SUM))

        grayScale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # smooth = cv2.GaussianBlur(grayScale, (5, 5), 1.5)

        edgesImage = cv2.Canny(grayScale, 50, 100)

        squares = findSquares(edgesImage)

        frame = frame

        print(len(squares))

        cv2.drawContours(frame, squares, -1, (0, 255, 0), 10)

        cv2.imshow(WINDOW_TITLE, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    videoCapture.release()
    cv2.destroyAllWindows()