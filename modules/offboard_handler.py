import asyncio
from mavsdk.offboard import (OffboardError, VelocityBodyYawspeed)

class OffboardHandler:
    target_captured = False
    target_coords = (0,0)
    yaw_diff = 0.0
    distance = 0.0
    StageHandler = None
    VisionHandler = None
    Drone = None

    async def trigger_offboard(self):
        while True:
            if(self.StageHandler.route == False):
                await self.yaw_capture()
                await self.goto_target()
            await asyncio.sleep(1)
    
    async def yaw_capture(self):
        await self.Drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

        print("-- Starting offboard")
        try:
            await self.Drone.offboard.start()
        except OffboardError as error:
            print(f"Starting offboard mode failed with error code: \
                {error._result.result}")
            print("-- Disarming")
            await self.Drone.action.disarm()
            return

        print("-- Turn in yaw angle direction")
        while (self.yaw_diff > 2 or self.yaw_diff < -2):
            await self.Drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(0.0, 0.0, 0.0, self.yaw_diff))
            await asyncio.sleep(1)
        print("-- Yaw diff less 2 deg")
        await self.Drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
        await asyncio.sleep(2)

    async def goto_target(self):
        while (self.VisionHandler.target_coords[1] > 10 or self.VisionHandler.target_coords[1] < -10):
            print(f"distance: {self.VisionHandler.target_coords[1]}")
            await self.Drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(0.5, 0.0, 0.0, 0.0))
            await asyncio.sleep(1)
        
        print("-- Target reached")
        await self.Drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
        await self.land_at_target()
        await asyncio.sleep(2)

    async def land_at_target(self):
        print("-- landing")
        while True:
            await self.Drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(0.0, 0.0, 2.0, 0.0))
            await asyncio.sleep(1)