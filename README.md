A computer vision exploration with a bunch of applications using a raspberry pi B+ and camera module.

Goals include keeping processing to a minimum in order to operate on the raspberry pi B+, yet provide effective analysis.

Learning from [OpenCV's python tutorials](https://docs.opencv.org/3.3.0/d6/d00/tutorial_py_root.html) and [Adrian Rosebrock's blog](https://www.pyimagesearch.com).

# Motion Detector
`motion_detection.py` using thresholding and absolute differences against a weighted average frame to detect and outline motion in a video feed.

# Red Color Detector
`red_color_detection.py` makes simple use of OpenCV's inRange to detect the color red in a video feed and outline the area.

# Camera Module Validation Scripts
`test_photo.py` and `test_video.py` are simple scripts to check if the camera module on the raspberry pi is functioning. `test_photo.py` takes a photo and `test_video.py` records a video feed.
