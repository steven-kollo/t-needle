#!/usr/bin/env python3

import cv2 as cv
import asyncio
from mavsdk import System
import modules.route_handler as route_handler
import modules.sensors_handler as sensors_handler
import modules.stage_handler as stage_handler
import modules.camera_handler as camera_handler
import modules.vision_handler as vision_handler
import modules.offboard_handler as offboard_handler
import pilot as pilot

RouteHandler = route_handler.RouteHandler()
SensorsHandler = sensors_handler.SensorsHandler()
StageHandler = stage_handler.StageHandler()
CameraHandler = camera_handler.CameraHandler()
VisionHandler = vision_handler.VisionHandler()
OffboardHandler = offboard_handler.OffboardHandler()

async def run():
    Drone = System()
    await Drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in Drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break
    
    async for health in Drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position state is good enough for flying.")
            break
    
        OffboardHandler.StageHandler = StageHandler
        OffboardHandler.VisionHandler = VisionHandler
        VisionHandler.StageHandler = StageHandler
        StageHandler.RouteHandler = RouteHandler
        StageHandler.SensorsHandler = SensorsHandler
        OffboardHandler.Drone = Drone
        VisionHandler.CameraHandler = CameraHandler
        OffboardHandler.VisionHandler = VisionHandler
        VisionHandler.OffboardHandler = OffboardHandler
        SensorsHandler.Drone = Drone
        StageHandler.Drone = Drone
        
    Pilot = pilot.Pilot(
        Drone=Drone
    )
    
    # Start parallel tasks
    asyncio.ensure_future(CameraHandler.read_sim_image())
    asyncio.ensure_future(SensorsHandler.update_position())
    asyncio.ensure_future(SensorsHandler.update_flight_mode())
    asyncio.ensure_future(StageHandler.update_target_point())
    asyncio.ensure_future(VisionHandler.process_image())
    asyncio.ensure_future(OffboardHandler.trigger_offboard())
    
    # Execute the maneuvers
    print("-- Arming")
    await Drone.action.arm()

    print("-- Taking off")
    await Drone.action.set_takeoff_altitude(10.0)
    await Drone.action.takeoff()    
    await asyncio.sleep(10)

    await Drone.action.goto_location(RouteHandler.target_point["lat"], RouteHandler.target_point["lon"], 500, 0)
    
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run())
