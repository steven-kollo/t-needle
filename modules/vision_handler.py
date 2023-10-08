import asyncio
import cv2 as cv
import numpy as np
import math
from imutils.object_detection import non_max_suppression
from scipy.spatial import distance as dist
from collections import OrderedDict

class VisionHandler:
    target = None
    target_detected = False
    target_captured = False
    target_coords = (0,0)
    target_yaw_angle = 0.0
    target_distance = 0.0
    tracker = None


    def __init__(self, Config):
        if (Config["sim_mode"]): 
            self.target = cv.imread(Config["sim_camera_config"]["target_img_path"], cv.COLOR_BGRA2RGB)
        else:
            pass

    async def process_image(self, CameraHandler, StageHandler):
        while True:    
            image = cv.cvtColor(CameraHandler.image, cv.COLOR_BGRA2RGB)
            template = self.target
            result = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
            
            threshold = 0.70
            (yCoords, xCoords) = np.where(result >= threshold)
            if StageHandler.stage == 3 and len(xCoords) > 0 and len(yCoords) > 0 and self.target_captured == False:
                if self.target_detected == False:
                    print("VISION: target detected")
                    print(f"x: {xCoords[0]} y: {yCoords[0]}")
                    self.target_detected = True
                elif self.validate_target(xCoords[0], yCoords[0]):
                    print("VISION: target captured")
                    print(f"x: {xCoords[0]} y: {yCoords[0]}")
                    self.tracker = cv.legacy.TrackerMedianFlow_create()
                    self.tracker.init(image, (xCoords[0], yCoords[0], 30, 30))
                    self.target_captured = True

            if self.target_captured == True:
                ok, bbox = self.tracker.update(image)
                if ok == True:
                    (x, y, w, h) = [int(v) for v in bbox]
                    cv.rectangle(image, (x, y), (x+w, y+h), (255, 255, 0), 1)
                    cv.putText(image, str('CAPTURE'), (10, 30), cv.QT_FONT_NORMAL, 1, (255, 255, 255))

            template_h, template_w = template.shape[:2]
            rects = []
            for (x, y) in zip(xCoords, yCoords):
                rects.append((x, y, x + template_w, y + template_h))
            pick = non_max_suppression(np.array(rects))

            for (startX, startY, endX, endY) in pick:
                cv.rectangle(image, (startX, startY), (endX, endY),(0, 255, 0), 2)
            cv.imshow('Results', image)
        
            if cv.waitKey(33) & 0xFF in (
                ord('q'), 
                27, 
            ):
                break
            await asyncio.sleep(0.1)

    def validate_target(self, xCoords, yCoords):
        x = abs(int(xCoords) - 200)
        y = abs(int(yCoords) - 200)
        if x < 150 and y < 150 and not self.target_captured:
            return True
             
    def calculate_distance_to_target(self):
        self.target_yaw_angle = round(math.atan2(self.target_coords[0], self.target_coords[1]) * 180 / math.pi, 2)
