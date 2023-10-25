# rpi 3b Debian Bookworm 64 bit

## Setup 
sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev libl
```
sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED
pip3 install opencv-python
pip3 install ultralytics
```

## test camera
https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/Libcamera-User-Guide/

```
libcamera-hello --help
libcamera-jpeg -o test.jpg
```

OpenCV test
```
from picamera2 import Picamera2
import time
import cv2 as cv

camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
camera.start()
time.sleep(0.1)

while True:
    im = camera.capture_array()
    
    cv.imshow("test", im)
    cv.waitKey(1)

```