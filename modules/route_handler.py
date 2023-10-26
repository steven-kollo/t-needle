import helpers
import asyncio
import math

class RouteHandler:
    point_i = 0
    route = None
    target_point = None
    checkpoint = None
    home = None

    async def update_target_point(self, Drone, SensorsHandler, StageHandler):
        while True:
            if not StageHandler.target_detected:
                await self.goto_target_point(Drone=Drone, SensorsHandler=SensorsHandler)
                distance = helpers.gps_to_meters(SensorsHandler.position["lat"], SensorsHandler.position["lon"], self.target_point[0], self.target_point[1])
                print(f"ROUTE: {round(distance, 2)} to point")
                if distance < 1.5:
                    print("ROUTE: point reached!")
                    self.next_point()
            await asyncio.sleep(1)

    async def goto_target_point(self, Drone, SensorsHandler):
        heading = await self.calculate_gps_heading(SensorsHandler)
        await Drone.action.goto_location(self.target_point[0], self.target_point[1], 505, heading)

    def next_point(self):
        if self.point_i < len(self.route) - 1:
            self.point_i += 1
            self.target_point = self.route[self.point_i]
        else:
            self.target_point = self.home
   
    async def calculate_gps_heading(self, SensorsHandler):
        position = SensorsHandler.position
        lat1 = (round(position["lat"], 5) * math.pi) / 180.0
        lon1 = (round(position["lon"], 5) * math.pi) / 180.0
        lat2 = (self.target_point[0] * math.pi) / 180.0
        lon2 = (self.target_point[1] * math.pi) / 180.0
        
        delta_lon = lon2 - lon1
        x = math.cos(lat2) * math.sin(delta_lon)
        y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
        heading = math.atan2(x, y)
        heading = (heading * 180.0) / math.pi
        if (heading < 0): 
            heading = 360.0 + heading

        return round(heading)

