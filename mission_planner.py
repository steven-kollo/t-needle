import math
import helpers

def build_area_points(start_pos, target_area):
    nearest_point_index = get_nearest_point(start_pos, target_area)
    get_nearest_point(target_area[nearest_point_index], target_area)
    mission = reorder_target_area(target_area)
    return mission

def plan_mission(start_pos, target_area):
    nearest_point_index = get_nearest_point(start_pos, target_area)
    get_nearest_point(target_area[nearest_point_index], target_area)
    target_area = reorder_target_area(target_area)
    mission = add_subpoints(target_area)
    return mission

def gps_to_meters(lat1, lon1, lat2, lon2): 
    R = 6378.137
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + \
    math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * \
    math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000

def get_nearest_point(start_pos, target_area):
    nearest_point_index = 0
    for i in range(len(target_area)):
        target_area[i]["distance"] = helpers.gps_to_meters(start_pos["lat"], start_pos["lon"], target_area[i]["lat"], target_area[i]["lon"])
        if (target_area[i]["distance"] < target_area[nearest_point_index]["distance"]):
            nearest_point_index = i
    return nearest_point_index

def reorder_target_area(target_area):
    target_area = sorted(target_area, key=lambda d: d["distance"])
    nearest_point = target_area[1]
    diagonal_point = target_area[3]

    target_area[1] = target_area[2]
    target_area[2] = diagonal_point
    target_area[3] = nearest_point 

    return target_area

def add_subpoints(target_area):
    segments_quantity = math.ceil(target_area[1]["distance"] / 5)
    side_a = divide_side(target_area[0], target_area[1], segments_quantity)
    side_b = divide_side(target_area[3], target_area[2], segments_quantity)
    mission = combine_sides(side_a, side_b)
    return mission

def divide_side(point_a, point_b, segments_quantity):
    shift_lat = round((point_b["lat"] - point_a["lat"]) / segments_quantity, 6)
    shift_lon = round((point_b["lon"] - point_a["lon"]) / segments_quantity, 6)
    divide_side_points = [point_a]
    for i in range(segments_quantity - 1):
        subpoint = {}
        subpoint["lat"] = round(divide_side_points[i]["lat"] + shift_lat, 6)
        subpoint["lon"] = round(divide_side_points[i]["lon"] + shift_lon, 6)
        divide_side_points.append(subpoint)
    divide_side_points.append(point_b)
    return divide_side_points

def combine_sides(side_a, side_b):
    mission = [side_a[0]]
    for i in range(len(side_a) - 1):
        if(i%2 == 0):
            mission.append(side_b[i])
            mission.append(side_b[i+1])
        else:
            mission.append(side_a[i])
            mission.append(side_a[i+1])
    mission.append(side_b[len(side_b) - 1])
    mission = pop_distance_item(mission)
    return mission

def pop_distance_item(mission):
    for item in mission:
        item.pop('distance', None)
    return mission
