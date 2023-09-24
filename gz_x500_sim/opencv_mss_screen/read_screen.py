import numpy as np
import cv2 as cv
import mss
from PIL import Image

with mss.mss() as sct:
    monitor = sct.monitors[1]
    while True:
        screenShot = sct.grab(monitor)
        img = Image.frombytes(
            'RGB', 
            (screenShot.width, screenShot.height), 
            screenShot.rgb, 
        )
        cropped = np.array(img)[650:1000, 1500:1900]
        cv.imshow('test', cropped)
        if cv.waitKey(33) & 0xFF in (
            ord('q'), 
            27, 
        ):
            break