import cv2
import numpy as np
import time
import os
import HandTracking as htm

def run_painter():
    debiljina_kista = 25
    eraserThickness = 100

    folderPath = "Header"
    myList = os.listdir(folderPath)
    print(myList)
    overlayList = []
    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)
    print(len(overlayList))
    header = overlayList[0]
    drawColor = (255, 0, 255)

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = htm.handDetector(detectionCon=0.65, maxHands=1)
    xp, yp = 0, 0
    imgCanvas = np.zeros((720, 1280, 3), np.uint8)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if not lmList == ([], []):
            xp, yp = 0, 0
            x1, y1 = lmList[0][8][1:]

            x2, y2 = lmList[0][12][1:]
            fingers = detector.fingersUp()
            if fingers[1] and fingers[2]:
                xp, yp = 0, 0
                print("biras")

                cv2.rectangle(img, (x1, y1 - 10), (x2, y2 + 10), drawColor, cv2.FILLED)
                if y1 < 125:
                    if 230 < x1 < 450:
                        header = overlayList[4]
                        drawColor = (255, 0, 255)
                    elif 550 < x1 < 750:
                        header = overlayList[2]
                        drawColor = (0, 255, 0)
                    elif 800 < x1 < 950:
                        header = overlayList[3]
                        drawColor = (255, 0, 0)
                    elif 1000 < x1 < 1200:
                        header = overlayList[4]
                        drawColor = (0, 0, 0)

            if fingers[1] and not fingers[2]:
                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                print("crtas")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, debiljina_kista)
                xp, yp = x1, y1

        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_or(img, imgCanvas)

        img[0:125, 0:1280] = header
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_painter()
