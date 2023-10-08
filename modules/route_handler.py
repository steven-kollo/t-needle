import helpers
import asyncio

class RouteHandler:
    area_reached = False
    target_point = None

    async def update_target_point(self, Drone, SensorsHandler):
        while True:
            if not self.area_reached:
                await self.go_to_area(Drone=Drone)
                distance = helpers.gps_to_meters(SensorsHandler.position["lat"], SensorsHandler.position["lon"], self.target_point["lat"], self.target_point["lon"])
                print(f"ROUTE: {round(distance, 2)} to point")
                if distance < 0.5:
                    print("ROUTE: point reached!")
                    self.area_reached = True
            await asyncio.sleep(1)

    async def go_to_area(self, Drone):
        await Drone.action.goto_location(self.target_point["lat"], self.target_point["lon"], self.target_point["alt"], 0)