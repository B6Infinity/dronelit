import cv2
import numpy as np

cap = cv2.VideoCapture('/dev/video2')

window_title = "FPV Live"
radius = 50

cv2.namedWindow(window_title)
cv2.setWindowProperty(window_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
while True:
    _, frame = cap.read()

    frame : np.ndarray

    center_x = frame.shape[1] // 2
    center_y = frame.shape[0] // 2


    # Process
    frame = cv2.rectangle(frame, (center_x - radius, center_y - radius), (center_x + radius, center_y + radius), (0, 0, 255) , 5) 
    
    cv2.imshow(window_title, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()