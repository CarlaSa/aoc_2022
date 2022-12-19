import math
from aocd import get_data, submit
import numpy as np
import re
from pprint import pp
from time import time
import copy
import multiprocessing as mp
from functools import partial, lru_cache


def process_data(test=False):
    if test:
        with open("input.txt") as f:
            data = f.read().split("\n")
    else:
        data = get_data(year=2022, day=19).split("\n")

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
        }
        # only can make 1 robot per minute -> don't need more than that
        blueprints[int(name)]["max_needed"] = {
            "ore": max(blueprints[int(name)][r]["ore"] for r in ["ore", "cla", "obs", "geo"]),
            "cla": max(blueprints[int(name)][r]["cla"] for r in ["ore", "cla", "obs", "geo"]),
            "obs": max(blueprints[int(name)][r]["obs"] for r in ["ore", "cla", "obs", "geo"]),
            "geo": 10000,
            "not": 21  # MAXMINUTES - blueprints[int(name)]["geo"]["obs"]
        }

    robots = {"not": 0, "ore": 1, "cla": 0, "obs": 0, "geo": 0}
    resources = {"ore": 0, "cla": 0, "obs": 0, "geo": 0}
    best_score = {key: -1 for key in blueprints}

    return blueprints, robots, resources, best_score


def back_tracking_wrapper(blueprint_key, blueprints, robots, resources, best_score, verbose=False, max_minutes=24):
    def possible_to_make(res, rob, blu):
        pos = dict()
        for rob_cost_name in ["not", "ore", "cla", "obs", "geo"]:
            if rob_cost_name != "not":
                rob_cost = blueprints[blu][rob_cost_name]
                b = all(res[i] - rob_cost[i] >= 0 for i in rob_cost.keys())  # if rob_cost[i] >= 0)
            else:
                b = True
            rob_max = blueprints[blu]["max_needed"][rob_cost_name]
            pos[rob_cost_name] = b and rob[rob_cost_name] <= rob_max
        if pos["geo"]:
            for key in ["not", "ore", "cla", "obs"]:
                pos[key] = False
        return pos

    def make_robot(rob_name, resources_, robots_, blu):
        if rob_name != "not":
            for res, val in blueprints[blu][rob_name].items():
                resources_[res] -= val
        robots_[rob_name] += 1
        return robots_, resources_

    states = dict()

    def no_better_states(robots_, resources_, minute_):
        def res_to_list(res):
            if isinstance(res, dict):
                return tuple(res.values())
            else:
                raise ValueError("???")

        res = res_to_list(resources_.copy())
        state = (tuple(robots_[k] for k in robots_ if k != "not"), minute_)
        if state not in states:
            states[state] = [res]
            return True
        else:
            res2_list = states[state]
            for res2 in res2_list:
                if all(res[i] <= res2[i] for i in range(4)):
                    return False
            states[state].append(res)
            return True

    def back_tracking(robots_, resources_, minute_, blueprint_id):
        # check which roboters are possible
        possibilities = possible_to_make(resources_, robots_, blueprint_id)

        # get resources:
        for rob_name, n in robots_.items():
            if rob_name != "not":
                resources_[rob_name] += n


        # cap rescources:
        resources_["ore"] = min(resources_["ore"], blueprints[blueprint_id]["max_needed"]["ore"] * 2)

        if minute_ == max_minutes:
            best_score[blueprint_id] = max(best_score[blueprint_id], resources_["geo"])
            return resources_["geo"], robots_, resources_

        # some things to stop early:

        # look if there were no runs with same minute & robots but less resources
        if not no_better_states(robots_, resources_, minute_):
            return -1, robots_, resources_

        # upper estimate score, break if low
        quad = lambda n: sum(i for i in range(n))
        upper_bound = resources_["geo"] + robots_["geo"] * (max_minutes +1 - minute_) + quad(max_minutes +1  - minute_)
        if upper_bound < best_score[blueprint_id]:
            return -1, robots_, resources_

        # is it still possible to get to geodes in this run?
        if robots_["geo"] == 0:
            upper_bound_obs = resources_["obs"] + robots_["obs"] * (max_minutes -1 - minute_) + quad(max_minutes -1 - minute_)
            if upper_bound_obs < blueprints[blueprint_id]["geo"]["obs"]:
                return -1, robots_, resources_

        score = -2
        ro_best, re_best = None, None
        for pos in [r for r in possibilities.keys() if possibilities[r]][::-1]:
            rob, res = make_robot(pos, copy.deepcopy(resources_), copy.deepcopy(robots_), blueprint_id)
            s, ro, re = back_tracking(copy.deepcopy(rob), copy.deepcopy(res), minute_ + 1, blueprint_id)
            if pos != "not":
                if robots_[pos] == 0:
                    i = ["ore", "cla", "obs", "geo"].index(pos)
            if s > score:
                score = s
                ro_best = ro
                re_best = re
            score = max(s, score)

        return score, ro_best, re_best

    start = time()
    s = back_tracking(copy.deepcopy(robots), copy.deepcopy(resources), 1, blueprint_key)
    if verbose:
        print(f"time bp {blueprint_key}: {time() - start} seconds")
    if s[0] < 0:
        score_ = 0
    else:
        score_ = blueprint_key * s[0]
    return [score_, blueprint_key, s[1], s[2]]


def part1(blueprints, robots, resources, best_score, verbose=False):
    f = partial(back_tracking_wrapper,
                blueprints=copy.deepcopy(blueprints),
                robots=copy.deepcopy(robots),
                resources=copy.deepcopy(resources),
                best_score=best_score,
                verbose=verbose)
    with mp.Pool(len(blueprints)) as pool:
        result = pool.map(f, blueprints.keys())

        result_ = {
            res[1]: {"robots": res[2], "ressources": res[3]} for res in sorted(result, key=lambda x: x[1])
        }
        if verbose:
            pp(result_)
        score = sum(result[i][0] for i in range(len(result)))
    return score


def part2(blueprints, robots, resources, verbose=True):
    blueprints_ = {k: blueprints[k] for k in blueprints if k in [1,2,3]}
    pp(blueprints_)
    best_score_ = {key: -1 for key in blueprints}

    f = partial(back_tracking_wrapper,
                blueprints=blueprints_,
                robots=robots,
                resources=resources,
                best_score=best_score_,
                verbose=verbose,
                max_minutes=32)

    with mp.Pool(len(blueprints_)) as pool:
        result = pool.map(f, blueprints_.keys())

        result_ = {
            res[1]: {"robots": res[2], "ressources": res[3]} for res in sorted(result, key=lambda x: x[1])
        }
        if verbose:
            pp(result_)
        s = [result_[i]["ressources"]["geo"] for i in result_]
        print(s)
        score = math.prod(s)
    return score


if __name__ == "__main__":
    TEST = False
    blueprints, robots, resources, best_score = process_data(test=TEST)
    start = time()
    sol1 = part1(blueprints, robots, resources, best_score, verbose= False)
    print(f"sol1: {sol1} \t in {time() - start} seconds")
    assert sol1 == 33 if TEST else sol1 == 1681

    start = time()
    sol2 = part2(blueprints, robots, resources)
    print(f"sol2: {sol2} \t in {time() - start} seconds")
    if not TEST:
        submit(sol2)