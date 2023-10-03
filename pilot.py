import asyncio
import helpers as helpers
import json
import modules.route_handler as route_handler
import modules.sensors_handler as sensors_handler
import modules.camera_handler as camera_handler
import modules.vision_handler as vision_handler
import modules.offboard_handler as offboard_handler
import modules.stage_handler as stage_handler

class Pilot:
    Drone = None
    Config = None
    RouteHandler = None
    SensorsHandler = None
    CameraHandler = None
    VisionHandler = None
    OffboardHandler = None
    StageHandler = None

    def __init__(self, Drone):
        self.Drone = Drone
        config_file = open('config.json')
        self.Config = json.load(config_file)
        config_file.close()
        
        # Modules
        self.RouteHandler = route_handler.RouteHandler(Config=self.Config)
        self.SensorsHandler = sensors_handler.SensorsHandler()
        self.CameraHandler = camera_handler.CameraHandler(Config=self.Config)
        self.VisionHandler = vision_handler.VisionHandler(Config=self.Config)
        self.OffboardHandler = offboard_handler.OffboardHandler()
        self.StageHandler = stage_handler.StageHandler()
        
        # Start parallel tasks
        asyncio.ensure_future(self.StageHandler.handle_stages(VisionHandler=self.VisionHandler))
        asyncio.ensure_future(self.SensorsHandler.update_position(Drone=self.Drone))
        asyncio.ensure_future(self.CameraHandler.read_sim_image())
        asyncio.ensure_future(self.VisionHandler.process_image(CameraHandler=self.CameraHandler))
        asyncio.ensure_future(self.OffboardHandler.trigger_offboard(StageHandler=self.StageHandler, VisionHandler=self.VisionHandler, Drone=self.Drone))
        asyncio.ensure_future(self.RouteHandler.update_target_point(Drone=self.Drone, SensorsHandler=self.SensorsHandler, StageHandler=self.StageHandler))
