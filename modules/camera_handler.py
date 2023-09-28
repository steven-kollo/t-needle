import asyncio
import numpy as np
import mss
from PIL import Image
import json

class CameraHandler:
    config = {}
    image = None
    sct = mss.mss()
    source = None

    def __init__(self):
        self.set_config()
        self.source = self.sct.monitors[1]
        screenShot = self.sct.grab(self.source)
        img = Image.frombytes(
            'RGB', 
            (screenShot.width, screenShot.height), 
            screenShot.rgb, 
        )
        self.image = np.array(img)[600:1000, 1500:1900]

    def set_config(self):
        config_file = open('config.json')
        config = json.load(config_file)
        if (config["sim_mode"]): 
            self.config = config["sim_camera_config"]
        else:
            self.config = config["camera_config"]
        config_file.close()

    async def read_sim_image(self):
        monitor = self.sct.monitors[1]
        while True:
            screenShot = self.sct.grab(monitor)
            img = Image.frombytes(
                'RGB', 
                (screenShot.width, screenShot.height), 
                screenShot.rgb, 
            )
            self.image = np.array(img)[600:1000, 1500:1900]
                
            await asyncio.sleep(0.1)

