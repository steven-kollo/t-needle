# t-needle

## Setup Ubuntu 22.04 | px4 v1.14.0-rc1
```
git clone --depth 1 --branch v1.14.0-rc1 https://github.com/PX4/PX4-Autopilot.git --recursive
bash ./PX4-Autopilot/Tools/setup/ubuntu.sh
```
reboot
```
pip3 install mavsdk
pip3 install aioconsole
git clone https://github.com/mavlink/MAVSDK-Python
git clone https://github.com/steven-kollo/t-needle
```
## Run simulation
```
cd ~/PX4-Autopilot
make px4_sitl_default gz_x500
```
## Run test T-Needle app
```
cd ~/t-needle
python3 main.py
```

