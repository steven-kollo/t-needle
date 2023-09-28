class RouteHandler:
    import modules.mission_planner as mission_planner
    import json
    start_pos = {}
    target_area = []
    mission = []
    point_i = 0
    target_point = {}

    def __init__(self):
        config_file = open('config.json')
        config = self.json.load(config_file)["mission"]
        self.start_pos = config["start_pos"]
        self.target_area = config["target_area"]
        config_file.close()
        self.mission = self.mission_planner.plan_mission(start_pos=self.start_pos, target_area=self.target_area)
        self.target_point = self.mission[0]

    def next_point(self):
        if self.point_i < len(self.mission) - 1:
            self.point_i += 1
            self.target_point = self.mission[self.point_i]
        else:
            self.target_point = self.start_pos
