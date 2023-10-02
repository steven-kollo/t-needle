import asyncio

class StageHandler:
    stage = 1

    # Consts
    STAGES = {
        "ROUTE": 1,
        "OFFBOARD": 2
    }

    def switch_stage(self, stage):
        if stage in self.STAGES:
            self.stage = self.STAGES[stage]
               
    async def handle_stages(self, VisionHandler):
        while True:
            # Switch to capturing
            if (VisionHandler.target_captured and self.stage != 2):
                self.switch_stage(stage="OFFBOARD")
                print(self.stage)
            await asyncio.sleep(1)
    
    
