import asyncio
import modules.helpers as helpers

class StageHandler:
    route = True
    RouteHandler = None
    SensorsHandler = None
    Drone = None

    async def update_target_point(self):
        while True:
            if self.route:
                position = self.SensorsHandler.position
                target = self.RouteHandler.target_point
                distance = helpers.gps_to_meters(position["lat"], position["lon"], target["lat"], target["lon"])
                print(distance)
                if distance < 0.5:
                    print("point reached!")
                    self.RouteHandler.next_point()
                    await self.Drone.action.goto_location(self.RouteHandler.target_point["lat"], self.RouteHandler.target_point["lon"], 500, 0)
            
            await asyncio.sleep(1)


    
    
