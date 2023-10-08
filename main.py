#!/usr/bin/env python3

import asyncio
from mavsdk import System
import pilot as pilot

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
        
    # Takeoff
    print("-- Arming")
    await Drone.action.arm()

    print("-- Taking off")
    await Drone.action.set_takeoff_altitude(7.0)
    await Drone.action.takeoff()    
    await asyncio.sleep(10)

    Pilot = pilot.Pilot(
        Drone=Drone
    )

    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run())
