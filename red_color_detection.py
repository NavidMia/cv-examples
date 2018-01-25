from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import imutils
import time
import numpy as np

def main():
    resolution = (640, 480)
    fps = 16
    min_contour_area = 500

    camera = PiCamera()
    camera.resolution = resolution
    camera.framerate = fps
    rawCapture = PiRGBArray(camera, size=resolution)
    time.sleep(1)

    redLowerBoundary = np.array((15, 15, 100), dtype = "uint8")
    redUpperBoundary = np.array((70, 70, 200), dtype = "uint8")

    print("Starting video capture, press 'q' to exit")
    for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = imutils.resize(f.array, width=500)
        # converting to hsv results in incorrect conversion
        # hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frame, redLowerBoundary, redUpperBoundary)
        
        output = cv2.bitwise_and(frame, frame, mask = mask)

        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    
        contours = contours[0] if imutils.is_cv2() else contours[1]

        for contour in contours:
            if cv2.contourArea(contour) < min_contour_area:
                continue

            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)


        cv2.imshow("Video Feed", frame)
        # cv2.imshow("HSV Feed", hsvFrame)
        # cv2.imshow("Color Feed", output)
        # cv2.imshow("Mask", mask)
        rawCapture.truncate(0)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
