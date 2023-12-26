import cv2
import numpy as np
import HandTracking as htm
import time
import pyautogui

def run_mouse_script():
    # Constants
    wCam, hCam = 640, 480
    frameR = 100  # Frame Reduction
    smoothening = 7

    # Variables
    pTime = 0
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    # Initialize camera and hand detector
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ne dela ti kamera")
        exit()

    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = htm.handDetector(maxHands=2)
    wScr, hScr = pyautogui.size()

    while True:
        # 1. Find hand Landmarks
        success, img = cap.read()
        img = detector.findHands(img)

        lmList, bbox = detector.findPosition(img, draw = False)

        # 2. Get the tip of the index and middle fingers
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            # 3. Check which fingers are up
            fingers = detector.fingersUp()

            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

            # 4. Only Index Finger: Moving Mode
            if fingers[1] == 1 and fingers[2] == 0:
                # 5. Convert Coordinates
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                # 6. Smoothen Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                # 7. Move Mouse
                pyautogui.moveTo(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY

            # 8. Both Index and middle fingers are up: Clicking Mode
            if fingers[1] == 1 and fingers[2] == 1:
                # 9. Find distance between fingers
                length, img, lineInfo = detector.findDistance(8, 12, img)

                # 10. Click mouse if distance short
                if length < 40:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    print("Klik")
                    pyautogui.click()

        # 11. Frame Rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        img = cv2.flip(img, 1)
        cv2.imshow("Image", img)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_mouse_script()
