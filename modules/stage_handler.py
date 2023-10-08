import asyncio
import mission_planner
class StageHandler:
    stage = None
    stages = {
        "ROUTE": 1,
        "GRID_YAW": 2,
        "GRID_ROUTE": 3,
        "CAPTURE": 4,
        "ACTION": 5,
        "NEXT_LINE": 6,
        "HOME": 7
    }

    def __init__(self, Config, RouteHandler):
        config = Config["mission"]
        self.grid_yaw = config["grid_yaw"]
        self.grid_step = config["grid_step"]
        self.min_relative_altitude = config["min_relative_altitude"]
        self.home = config["home"]
        self.target_area = mission_planner.build_area_points(start_pos=self.home, target_area=config["target_area"])
        RouteHandler.target_point = self.target_area[0]


    async def handle_stages(self, RouteHandler, OffboardHandler, VisionHandler):
        while True:
            if not RouteHandler.area_reached and self.stage != 1:
                self.switch_stage(stage="ROUTE")
            elif (RouteHandler.area_reached and self.stage == 1):
                self.switch_stage(stage="GRID_YAW")
            elif (OffboardHandler.grid_yaw and self.stage == 2):
                self.switch_stage(stage="GRID_ROUTE")
            elif (VisionHandler.target_captured and self.stage == 3):
                self.switch_stage(stage="CAPTURE")
            await asyncio.sleep(1)
    
    def switch_stage(self, stage):
        if stage in self.stages:
            self.stage = self.stages[stage]
            print(f"STAGE: {stage}")
    
                   
