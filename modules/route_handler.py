import mission_planner
import helpers
import asyncio

class RouteHandler:
    start_pos = {}
    target_area = []
    mission = []
    point_i = 0
    target_point = {}

    def __init__(self, Config):
        config = Config["mission"]
        self.start_pos = config["start_pos"]
        self.target_area = config["target_area"]
        self.mission = mission_planner.plan_mission(start_pos=self.start_pos, target_area=self.target_area)
        self.target_point = self.mission[0]

    def next_point(self):
        if self.point_i < len(self.mission) - 1:
            self.point_i += 1
            self.target_point = self.mission[self.point_i]
        else:
            self.target_point = self.start_pos
    
    async def update_target_point(self, Drone, SensorsHandler, StageHandler):
        while True:
            # "ROUTE": 1
            if StageHandler.stage == 1:
                distance = helpers.gps_to_meters(SensorsHandler.position["lat"], SensorsHandler.position["lon"], self.target_point["lat"], self.target_point["lon"])
                print(f"ROUTE: {round(distance, 2)} to point")
                if distance < 0.5:
                    print("ROUTE: point reached!")
                    self.next_point()
                    await Drone.action.goto_location(self.target_point["lat"], self.target_point["lon"], 500, 0)
            
            await asyncio.sleep(1)