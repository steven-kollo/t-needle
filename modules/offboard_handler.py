import asyncio
from mavsdk.offboard import (OffboardError, VelocityBodyYawspeed)

class OffboardHandler:
    target_captured = False
    target_coords = (0,0)
    yaw_diff = 0.0
    distance = 0.0

    async def trigger_offboard(self, StageHandler, VisionHandler, Drone):
        while True:
            # "OFFBOARD": 2
            if StageHandler.stage == 2:
                await self.yaw_capture(Drone=Drone, VisionHandler=VisionHandler)
                await self.goto_target(Drone=Drone, VisionHandler=VisionHandler)
            await asyncio.sleep(1)
    
    async def yaw_capture(self, Drone, VisionHandler):
        await Drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

        print("-- Starting offboard")
        try:
            await Drone.offboard.start()
        except OffboardError as error:
            print(f"Starting offboard mode failed with error code: \
                {error._result.result}")
            print("-- Disarming")
            await Drone.action.disarm()
            return

        print("-- Turn in yaw angle direction")
        while (VisionHandler.target_yaw_angle > 2 or VisionHandler.target_yaw_angle < -2):
            await Drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(0.0, 0.0, 0.0, VisionHandler.target_yaw_angle))
            await asyncio.sleep(1)
        print("-- Yaw diff less 2 deg")
        await Drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
        await asyncio.sleep(2)

    async def goto_target(self, Drone, VisionHandler):
        while (VisionHandler.target_coords[1] > 10 or VisionHandler.target_coords[1] < -10):
            print(f"distance: {VisionHandler.target_coords[1]}")
            await Drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(0.5, 0.0, 0.0, 0.0))
            await asyncio.sleep(1)
        
        print("-- Target reached")
        await Drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
        await self.land_at_target(Drone=Drone)
        await asyncio.sleep(2)

    async def land_at_target(self, Drone):
        print("-- landing")
        while True:
            await Drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(0.0, 0.0, 2.0, 0.0))
            await asyncio.sleep(1)