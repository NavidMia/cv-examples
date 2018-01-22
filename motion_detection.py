from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import imutils
import time

deltaThreshold = 5
resolution = (640, 480)
fps = 32
min_contour_area = 500

camera = PiCamera()
camera.resolution = resolution
camera.framerate = fps
rawCapture = PiRGBArray(camera, size=resolution)
time.sleep(1)

avgFrame = None

print("Starting video capture, press 'q' to exit")

for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = f.array
    motionStatus = ""

    # resize frame since processing on large raw image is costly/unnecessary
    frame = imutils.resize(frame, width=500)

    # grayscale since threshold/delta is used for detection
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # blur to smooth out high freq noise
    grayscale = cv2.GaussianBlur(grayscale, (21, 21), 0)

    if avgFrame is None:
        avgFrame = grayscale.copy().astype("float")
        rawCapture.truncate(0)
        continue

    # weighted avg of frames to check against for motion
    cv2.accumulateWeighted(grayscale, avgFrame, 0.5)
    # delta of current frame and avg frame
    frameDelta = cv2.absdiff(grayscale, cv2.convertScaleAbs(avgFrame))

    # threshold to amplify differences in the delta frame
    threshold = cv2.threshold(frameDelta, deltaThreshold, 255, cv2.THRESH_BINARY)[1]
    # dilate to smooth and avoid noise
    threshold = cv2.dilate(threshold, None, iterations=2)

    # detect contours
    contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    
    contours = contours[0] if imutils.is_cv2() else contours[1]

    # if there is a significant change, show motion is detected
    for contour in contours:
        if cv2.contourArea(contour) < min_contour_area:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        motionStatus = "Motion Detected"

    cv2.putText(frame, motionStatus, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Video Feed", frame)
    # cv2.imshow("Theshold", threshold)
    # cv2.imshow("Frame Delta", frameDelta) 
    rawCapture.truncate(0)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
