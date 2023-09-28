class SensorsHandler:
    position = {"lat": 0.0, "lon": 0.0}
    flight_mode = None

    async def update_position(self, drone):
        async for position in drone.telemetry.position():
            lat = round(position.latitude_deg, 5)
            lon = round(position.longitude_deg, 5)
            
            if lon + lat != self.position["lat"] + self.position["lon"]:
                self.position["lat"] = lat
                self.position["lon"] = lon
                

    async def update_flight_mode(self, drone):
        async for flight_mode in drone.telemetry.flight_mode():
            if flight_mode != self.flight_mode:
                self.flight_mode = flight_mode
