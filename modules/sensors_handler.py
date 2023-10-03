class SensorsHandler:
    position = {"lat": 0.0, "lon": 0.0}

    async def update_position(self, Drone):
        async for position in Drone.telemetry.position():
            lat = round(position.latitude_deg, 5)
            lon = round(position.longitude_deg, 5)
            
            if lon + lat != self.position["lat"] + self.position["lon"]:
                self.position["lat"] = lat
                self.position["lon"] = lon
                

    
