import helpers
import asyncio
import math

class RouteHandler:
    area_reached = False
    target_point = None

    async def update_target_point(self, Drone, SensorsHandler):
        while True:
            if not self.area_reached:
                await self.go_to_area(Drone=Drone, SensorsHandler=SensorsHandler)
                distance = helpers.gps_to_meters(SensorsHandler.position["lat"], SensorsHandler.position["lon"], self.target_point["lat"], self.target_point["lon"])
                print(f"ROUTE: {round(distance, 2)} to point")
                if distance < 0.5:
                    print("ROUTE: point reached!")
                    self.area_reached = True
            await asyncio.sleep(1)

    async def go_to_area(self, Drone, SensorsHandler):
        heading = await self.calculate_gps_heading(SensorsHandler)
        print(heading)
        await Drone.action.goto_location(self.target_point["lat"], self.target_point["lon"], self.target_point["alt"], heading)
    
    async def calculate_gps_heading(self, SensorsHandler):
        position = SensorsHandler.position
        lat1 = (round(position["lat"], 5) * math.pi) / 180.0
        lon1 = (round(position["lon"], 5) * math.pi) / 180.0
        lat2 = (self.target_point["lat"] * math.pi) / 180.0
        lon2 = (self.target_point["lon"] * math.pi) / 180.0
        
        
        delta_lon = lon2 - lon1
        x = math.cos(lat2) * math.sin(delta_lon)
        y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
        heading = math.atan2(x, y)
        heading = (heading * 180.0) / math.pi
        if (heading < 0): 
            heading = 360.0 + heading

        return round(heading)

