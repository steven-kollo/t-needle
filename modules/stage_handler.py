import asyncio
import mission_planner
import mission_plannerV2
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

        # self.target_area = mission_planner.build_area_points(start_pos=self.home, target_area=config["target_area"])
        self.route_points = mission_plannerV2.build_mission(self.home, config["target_area"], 0.00008)
        # self.route_points = mission_planner.plan_mission(start_pos=self.home, target_area=config["target_area"])
        RouteHandler.route = self.route_points
        print(RouteHandler.route)
        RouteHandler.target_point = self.route_points[0]
        RouteHandler.home = self.home


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
    
                   
