import asyncio
import cv2 as cv
import json
import math

class VisionHandler:
    target = None
    target_captured = False
    target_coords = (0,0)
    target_yaw_angle = 0.0

    # TODO make an option for physical camera
    def __init__(self, Config):
        if (Config["sim_mode"]): 
            self.target = cv.imread(Config["sim_camera_config"]["target_img_path"], cv.IMREAD_UNCHANGED)
        else:
            pass

    async def process_image(self, CameraHandler):
        while True:    
            image = CameraHandler.image
            target = self.target

            result = cv.matchTemplate(image, target, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if (max_val > 0.8): 
                top_left = max_loc
                center = (top_left[0] + int(target.shape[1] / 2), top_left[1] + int(target.shape[1] / 2))
                bottom_right = (top_left[0] + target.shape[1], top_left[1] + target.shape[1])
                cv.rectangle(image, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)
                self.target_captured = True
                self.target_coords = (center[0] - 200, 200 - center[1])
                self.target_yaw_angle = round(math.atan2(self.target_coords[0], self.target_coords[1]) * 180 / math.pi, 2)
                # self.OffboardHandler.yaw_diff = self.target_yaw_angle

            cv.imshow('CV', image)
            if cv.waitKey(33) & 0xFF in (
                ord('q'), 
                27, 
            ):
                break
            await asyncio.sleep(0.1)

