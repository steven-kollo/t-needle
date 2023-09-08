#!/usr/bin/env python3

import asyncio
from mavsdk import System

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
    print_position_task = asyncio.ensure_future(print_position(drone))
    print_flight_mode_task = asyncio.ensure_future(print_flight_mode(drone))


    running_tasks = [print_position_task, print_flight_mode_task]
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
    await drone.action.set_takeoff_altitude(10.0)
    await drone.action.takeoff()

    await asyncio.sleep(10)

    await drone.action.goto_location(28.4526, -13.86714, 500, 0)

    while True:
        # TODO Why coord reached
        print("Staying connected, press Ctrl-C to exit")
        await asyncio.sleep(1)

    print("-- Landing")
    await drone.action.land()

    # Wait until the drone is landed (instead of exiting after 'land' is sent)
    await termination_task


async def print_position(drone):
    """ Prints the coords when it changes """

    previous_lat = 0
    previous_lon = 0
    previous_altitude = None

    async for position in drone.telemetry.position():
        lat = round(position.latitude_deg, 5)
        lon = round(position.longitude_deg, 5)
        altitude = round(position.relative_altitude_m)

        if altitude != previous_altitude:
            previous_altitude = altitude
            print(f"Altitude: {altitude}")

        if lon + lat != previous_lat + previous_lon:
            previous_lat = lat
            previous_lon = lon
            print(f"Lat: {lat}, lon: {lon}")


async def print_flight_mode(drone):
    """ Prints the flight mode when it changes """

    previous_flight_mode = None

    async for flight_mode in drone.telemetry.flight_mode():
        if flight_mode != previous_flight_mode:
            previous_flight_mode = flight_mode
            print(f"Flight mode: {flight_mode}")


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