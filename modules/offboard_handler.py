import asyncio
from mavsdk.offboard import (OffboardError, VelocityBodyYawspeed, VelocityNedYaw)

class OffboardHandler:
    grid_yaw = False
    target_captured = False
    target_coords = (0,0)
    yaw_diff = 0.0
    distance = 0.0

    async def handle_offboard(self, StageHandler, VisionHandler, SensorsHandler, Drone):
        while True:
            # "GRID_YAW": 2
            if StageHandler.stage == 2:
                await self.turn_to_grid_yaw(Drone=Drone, SensorsHandler=SensorsHandler, yaw=StageHandler.grid_yaw)
                self.grid_yaw = True
            # "GRID_ROUTE": 3
            elif StageHandler.stage == 3:
                await self.fly_grid_route(Drone=Drone, VisionHandler=VisionHandler)
            # "CAPTURE": 4
            elif StageHandler.stage == 4:
                pass
            await asyncio.sleep(1)
    
    async def turn_to_grid_yaw(self, Drone, SensorsHandler, yaw):
        await Drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
        await Drone.offboard.start()

        print("OFFBOARD: to grid yaw")
        while SensorsHandler.heading > yaw + 0.2 or SensorsHandler.heading < yaw - 0.2:
            await Drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, yaw))
            await asyncio.sleep(2)

    async def fly_grid_route(self, Drone, VisionHandler):
        while (VisionHandler.target_detected == False):
            await Drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(2.0, 0.0, 0.0, 0.0))
            await asyncio.sleep(1)

        await self.change_velocity(Drone, 2.0, 0.5, 0.4)

        while (VisionHandler.target_captured == False):
            await Drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(0.5, 0.0, 0.0, 0.0))
            await asyncio.sleep(1)
        await self.change_velocity(Drone, 0.5, 0.0, 0.2)
        print("OFFBOARD: stop on captured target")
        await Drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
        await asyncio.sleep(2)

    async def yaw_capture(self, Drone, VisionHandler):
        await Drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

        print("OFFBOARD: starting offboard")
        try:
            await Drone.offboard.start()
        except OffboardError as error:
            print(f"Starting offboard mode failed with error code: \
                {error._result.result}")
            print("OFFBOARD: disarming")
            await Drone.action.disarm()
            return

        print("OFFBOARD: turn in yaw angle direction")
        while (VisionHandler.target_yaw_angle > 2 or VisionHandler.target_yaw_angle < -2):
            await Drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(0.0, 0.0, 0.0, VisionHandler.target_yaw_angle))
            await asyncio.sleep(1)
        print("OFFBOARD: yaw diff less 2 deg")
        await Drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
        await asyncio.sleep(2)

    async def change_velocity(self, Drone, curr_v, new_v, sec):
        step = (new_v - curr_v) / 4
        for n in range(4):
            print(f"vel: {curr_v + step * n}")
            await Drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(curr_v + step * n, 0.0, 0.0, 0.0))
            await asyncio.sleep(sec / 4)
        
        