#!/usr/bin/env python3

import asyncio
from mavsdk import System
import modules.mission_handler as mission_handler
import modules.sensors_handler as sensors_handler
import modules.stage_handler as stage_handler

MissionHandler = mission_handler.MissionHandler()
SensorsHandler = sensors_handler.SensorsHandler()
StageHandler = stage_handler.StageHandler()

async def run():
    # Init the drone
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    # Start parallel tasks
    print_position_task = asyncio.ensure_future(SensorsHandler.update_position(drone=drone))
    print_flight_mode_task = asyncio.ensure_future(SensorsHandler.update_flight_mode(drone=drone))
    update_target_point_task = asyncio.ensure_future(StageHandler.update_target_point(SensorsHandler=SensorsHandler, MissionHandler=MissionHandler, drone=drone))

    running_tasks = [print_position_task, print_flight_mode_task, update_target_point_task]
    termination_task = asyncio.ensure_future(
        observe_is_in_air(drone, running_tasks))

    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position state is good enough for flying.")
            break

    # Execute the maneuvers
    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.set_takeoff_altitude(3.0)
    await drone.action.takeoff()

    await asyncio.sleep(10)
    altitude = 3.0
    mission = MissionHandler.mission
    await drone.action.goto_location(MissionHandler.target_point["lat"], MissionHandler.target_point["lon"], 495, 0)
    # print(mission[1])
    # await MissionHandler.go_to_point(drone=drone)
    # await drone.action.goto_location(mission[1]["lat"], mission[1]["lon"], 495, 0)
    await asyncio.sleep(10)
    # await drone.action.goto_location(mission[2]["lat"], mission[2]["lon"], 495, 0)
    # await asyncio.sleep(10)
    # await drone.action.goto_location(mission[3]["lat"], mission[3]["lon"], 495, 0)
    # await asyncio.sleep(10)

    while True:
        #if (mission[counter]["lat"] + mission[counter]["lon"] == )
        # TODO Why coord reached
        #print("Staying connected, press Ctrl-C to exit")
        # print(SensorsHandler.position)
        await asyncio.sleep(1)

    print("-- Landing")
    await drone.action.land()

    # Wait until the drone is landed (instead of exiting after 'land' is sent)
    await termination_task

async def observe_is_in_air(drone, running_tasks):
    """ Monitors whether the drone is flying or not and
    returns after landing """

    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            for task in running_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            await asyncio.get_event_loop().shutdown_asyncgens()
            return


if __name__ == "__main__":
    # Start the main function
    asyncio.run(run())