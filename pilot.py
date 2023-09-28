import modules.route_handler as route_handler
import modules.sensors_handler as sensors_handler
import modules.stage_handler as stage_handler
import modules.camera_handler as camera_handler
import modules.vision_handler as vision_handler
import modules.offboard_handler as offboard_handler

class Pilot:
    Drone=None
    RouteHandler = route_handler.RouteHandler()
    SensorsHandler = sensors_handler.SensorsHandler()
    StageHandler = stage_handler.StageHandler()
    CameraHandler = camera_handler.CameraHandler()
    VisionHandler = vision_handler.VisionHandler()
    OffboardHandler = offboard_handler.OffboardHandler()

    def __init__(self, Drone):
        self.Drone=Drone
    
    
    