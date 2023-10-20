# rpi 3b Debian Bookworm

## Setup opencv
```
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libgtk2.0-dev libgtk-3-dev
sudo apt-get install libatlas-base-dev gfortran
```
reboot
```
sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
cd ~/Downloads
wget https://www.python.org/ftp/python/3.9/Python-3.9.tgz`
sudo tar zxf Python-3.9.tgz
cd Python-3.9
sudo ./configure --enable-optimizations
sudo make -j 2
sudo make altinstall
echo "alias python=/usr/local/bin/python3.9" >> ~/.bashrc
source ~/.bashrc
alias python3=python3.9
```
```
sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED
pip3 install opencv-python==4.7.0.72
pip3 install ultralytics
# if hashes missmatch
pip3 install opencv-python==4.7.0.72 --no-cache-dir
pip3 install matplotlib --no-cache-dir
pip3 install scipy --no-cache-dir
pip3 install ultralytics --no-cache-dir
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