import cv2
import numpy as np
from PIL import Image

video_capture = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
w = int(video_capture.get(3))
h = int(video_capture.get(4))
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi', fourcc, 15, (w, h))

while True:
    ret, frame = video_capture.read()  # frame shape 640*480*3
    if ret != True:
        break
    cv2.imshow('video', frame)
    out.write(frame)
    # Press Q to stop!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
out.release()
cv2.destroyAllWindows()