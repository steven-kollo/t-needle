import asyncio
import mission_planner
class StageHandler:
    target_detected = False
    target_captured = False
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
        self.route_points = mission_planner.build_mission(self.home, config["target_area"], config["offset"])
        RouteHandler.route = self.route_points
        RouteHandler.target_point = self.route_points[0]
        RouteHandler.home = self.home


    async def handle_stages(self):
        while True:
            if not self.target_captured and self.stage != 1:
                self.switch_stage(stage="ROUTE")
            elif (self.target_captured and self.stage == 1):
                self.switch_stage(stage="CAPTURE")
                self.target_captured = True
            
            await asyncio.sleep(0.05)
    
    def switch_stage(self, stage):
        if stage in self.stages:
            self.stage = self.stages[stage]
            print(f"STAGE: {stage}")
    
                   
