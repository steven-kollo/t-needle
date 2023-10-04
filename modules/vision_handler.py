import asyncio
import cv2 as cv
import math

class VisionHandler:
    target = None
    target_captured = False
    target_coords = (0,0)
    target_yaw_angle = 0.0
    target_distance = 0.0

    # TODO make an option for physical camera
    def __init__(self, Config):
        if (Config["sim_mode"]): 
            self.target = cv.imread(Config["sim_camera_config"]["target_img_path"], cv.IMREAD_UNCHANGED)
        else:
            pass

    async def process_image(self, CameraHandler):
        while True:    
            image = cv.cvtColor(CameraHandler.image, cv.COLOR_BGRA2RGB)
            # cv.cvtColor(CameraHandler.image, cv.COLOR_BGRA2RGB)
            target = self.target

            result = cv.matchTemplate(image, target, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            
            if self.validate_target(max_val, max_loc): 
                center = (max_loc[0] + int(target.shape[1] / 2), max_loc[1] + int(target.shape[1] / 2))
                cv.circle(image, center=center, radius=20, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)
                self.target_coords = (center[0] - 200, 200 - center[1])
                self.calculate_distance_to_target()
                

            cv.imshow('CV', image)
            if cv.waitKey(33) & 0xFF in (
                ord('q'), 
                27, 
            ):
                break
            await asyncio.sleep(0.1)

    def validate_target(self, max_val, max_loc):
        if self.target_captured:
            return True
        if (max_val > 0.8):
            x = abs(int(max_loc[0]) - 200)
            y = abs(int(max_loc[1]) - 200)
            if x < 150 and y < 150 and not self.target_captured:
                self.target_captured = True
                print("VISION: target captured")
                return True
             
    def calculate_distance_to_target(self):
        self.target_yaw_angle = round(math.atan2(self.target_coords[0], self.target_coords[1]) * 180 / math.pi, 2)
