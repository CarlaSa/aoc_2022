from aocd import get_data, submit
import numpy as np
import re
from pprint import pp
import copy

data = get_data(year=2022, day=19).split("\n")

# with open("input.txt") as f:
#     data = f.read().split("\n")


def string_to_cost(s):
    x = {o: 0 for o in ["ore", "cla", "obs", "geo"]}
    x.update({ss.split(" ")[1][0:3]: int(ss.split(" ")[0]) for ss in s.split(" and ")})
    return x


blueprints = dict()
for d in data:
    name = re.search(r"Blueprint (\d+)", d)[1]
    ore_rob_cost = re.search(r"Each ore robot costs ([^.]*)", d)[1]
    cla_rob_cost = re.search(r"Each clay robot costs ([^.]*)", d)[1]
    obs_rob_cost = re.search(r"Each obsidian robot costs ([^.]*)", d)[1]
    geo_rob_cost = re.search(r"Each geode robot costs ([^.]*)", d)[1]
    blueprints[int(name)] = {
        "ore": string_to_cost(ore_rob_cost),
        "cla": string_to_cost(cla_rob_cost),
        "obs": string_to_cost(obs_rob_cost),
        "geo": string_to_cost(geo_rob_cost),
        "fastest": [0, 100, 100, 100]
    }
    # only can make 1 robot per minute -> don't need more than
    blueprints[int(name)]["max_needed"] = {
        "ore": max(blueprints[int(name)][r]["ore"] for r in ["ore", "cla", "obs", "geo"]),
        "cla": max(blueprints[int(name)][r]["cla"] for r in ["ore", "cla", "obs", "geo"]),
        "obs": max(blueprints[int(name)][r]["obs"] for r in ["ore", "cla", "obs", "geo"]),
        "geo": 1000,
        "not": 10
    }

robots = {
    "not": 0, "ore": 1, "cla": 0, "obs": 0, "geo": 0
}

resources = {
    "ore": 0, "cla": 0, "obs": 0, "geo": 0
}


def possible_to_make(res, rob, blu):
    global blueprints
    pos = dict()
    for rob_cost_name in ["not","ore", "cla", "obs", "geo"]:
        if rob_cost_name != "not":
            rob_cost = blueprints[blu][rob_cost_name]
            b = all(res[i] - rob_cost[i] > 0 for i in rob_cost.keys() if rob_cost[i] > 0)
        else:
            b = True
        rob_max = blueprints[blu]["max_needed"][rob_cost_name]
        pos[rob_cost_name] = b and rob[rob_cost_name] <= rob_max
    return pos


def make_robot(rob_name, resources_, robots_, blu):
    if rob_name != "not":
        for res, val in blueprints[blu][rob_name].items():
            resources_[res] -= val
    robots_[rob_name] += 1
    return robots_, resources_


MAXMINUTES = 24
PATHS = 0
ROBOT_MAX = 6


def back_tracking(robots_, resources_, minute_, blueprint_id):
    global  PATHS
    global blueprints

    if minute_ == MAXMINUTES:
        return resources_["geo"], robots_, resources_

    # get resources:
    for rob_name, n in robots_.items():
        if rob_name != "not":
            resources_[rob_name] += n

    # some things to stop early:
    t_to_geo = blueprints[blueprint_id]["fastest"][3] + 0
    t_to_obs = blueprints[blueprint_id]["fastest"][2] + 2
    t_to_cla = blueprints[blueprint_id]["fastest"][1] + 2
    #print(t_to_geo, t_to_obs, t_to_cla)  # 20 17 10 # 6 11 20 # 18, 15, 8

    #t_to_geo,t_to_obs , t_to_cla = 20, 11, 6
    if minute_ >= t_to_geo and robots_["geo"] == 0:
        return -1, robots_, resources_
    if minute_ >= t_to_obs and robots_["obs"] == 0:
        return -1, robots_, resources_
    if minute_ >= t_to_cla and robots_["cla"] == 0:
        return -1, robots_, resources_




    possibilities = possible_to_make(resources_, robots_, blueprint_id)

    score = -2
    ro_best, re_best = None, None
    for pos in [r for r in possibilities.keys() if possibilities[r]][::-1]:
        PATHS += 1
        rob, res = make_robot(pos, copy.deepcopy(resources_), copy.deepcopy(robots_), blueprint_id)
        s, ro, re = back_tracking(copy.deepcopy(rob), copy.deepcopy(res), minute_ + 1, blueprint_id)
        if pos != "not":
            if robots_[pos] == 0:
                i = ["ore", "cla", "obs", "geo"].index(pos)
                blueprints[blueprint_id]["fastest"][i] = min(blueprints[blueprint_id]["fastest"][i], minute_ +1)
        if s > score:
            score = s
            ro_best = ro
            re_best = re
        score = max(s, score)
    return score, ro_best, re_best

quality_level = 0
for key in blueprints.keys():
    #if blueprints[key]["geo"]["obsidian"]
    s = back_tracking(copy.deepcopy(robots), copy.deepcopy(resources), 1, key)
    quality_level += key * s[0]
    #print(PATHS)
    #PATHS = 0
    print(s)
    #print(blueprints[key]["fastest"])

pp(blueprints)
submit(quality_level)
