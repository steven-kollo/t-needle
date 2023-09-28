import asyncio
import modules.helpers as helpers

class StageHandler:
    route = True

    async def update_target_point(self, MissionHandler, SensorsHandler, drone):
        while True:
            if self.route:
                position = SensorsHandler.position
                target = MissionHandler.target_point
                distance = helpers.gps_to_meters(position["lat"], position["lon"], target["lat"], target["lon"])
                print(distance)
                if distance < 0.5:
                    print("point reached!")
                    MissionHandler.next_point()
                    await drone.action.goto_location(MissionHandler.target_point["lat"], MissionHandler.target_point["lon"], 500, 0)
            
            await asyncio.sleep(1)


    
    
