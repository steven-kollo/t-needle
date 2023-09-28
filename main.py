#!/usr/bin/env python3

import cv2 as cv
import asyncio
from mavsdk import System
import modules.mission_handler as mission_handler
import modules.sensors_handler as sensors_handler
import modules.stage_handler as stage_handler
import modules.camera_handler as camera_handler
import modules.vision_handler as vision_handler
import modules.offboard_handler as offboard_handler

MissionHandler = mission_handler.MissionHandler()
SensorsHandler = sensors_handler.SensorsHandler()
StageHandler = stage_handler.StageHandler()
CameraHandler = camera_handler.CameraHandler()
VisionHandler = vision_handler.VisionHandler(StageHandler=StageHandler)
OffboardHandler = offboard_handler.OffboardHandler(VisionHandler=VisionHandler, StageHandler=StageHandler)

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break
    OffboardHandler.drone = drone
    VisionHandler.CameraHandler = CameraHandler
    OffboardHandler.VisionHandler = VisionHandler
    VisionHandler.OffboardHandler = OffboardHandler
    # Start parallel tasks
    asyncio.ensure_future(CameraHandler.read_sim_image())
    asyncio.ensure_future(SensorsHandler.update_position(drone=drone))
    asyncio.ensure_future(SensorsHandler.update_flight_mode(drone=drone))
    asyncio.ensure_future(StageHandler.update_target_point(SensorsHandler=SensorsHandler, MissionHandler=MissionHandler, drone=drone))
    asyncio.ensure_future(VisionHandler.process_image())
    asyncio.ensure_future(OffboardHandler.trigger_offboard())
    
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position state is good enough for flying.")
            break

    # Execute the maneuvers
    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.set_takeoff_altitude(10.0)
    await drone.action.takeoff()    
    await asyncio.sleep(10)

    await drone.action.goto_location(MissionHandler.target_point["lat"], MissionHandler.target_point["lon"], 500, 0)
    
    while True:
        await asyncio.sleep(1)

    print("-- Landing")
    await drone.action.land()



if __name__ == "__main__":
    asyncio.run(run())
