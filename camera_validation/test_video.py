from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time

camera = PiCamera()
resolution = (640, 480)
camera.resolution = resolution
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=resolution)
time.sleep(0.1)

print("Starting video capture, press 'q' to exit")

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array

	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
	
	rawCapture.truncate(0)

	if key == ord("q"):
		break

cv2.destroyAllWindows()
