from aocd import get_data, submit
import numpy as np
from pprint import pp
from math import prod
from time import time

data = get_data(year=2022, day=11).split("Monkey ")


def to_lambda(s):
    return eval("lambda old: " + s.split("=")[1])


def parse_data():
    monkeys_ = list()
    for d in data[1:]:
        monkey_dict = {}
        d = d.split("\n")
        monkey_dict["name"] = int(d[0][:-1])
        monkey_dict["items"] = [int(dd) for dd in d[1].split(":")[1].split(",")]
        monkey_dict["operation"] = to_lambda(d[2].split(":")[1])
        monkey_dict["test_div"] = int(d[3].split("divisible by ")[1])
        monkey_dict["case_true"] = int(d[4].split("monkey ")[1])
        monkey_dict["case_false"] = int(d[5].split("monkey ")[1])
        monkey_dict["n_inspected"] = 0
        assert len(monkeys_) == monkey_dict["name"]
        monkeys_.append(monkey_dict)
    return monkeys_


def loop_trough(n, operation, monkeys):
    for _ in range(n):
        for monkey in monkeys:
            while len(monkey["items"]) > 0:
                item = monkey["items"].pop()
                item = monkey["operation"](item)
                item = operation(item)
                if item % monkey["test_div"] == 0:
                    monkeys[monkey["case_true"]]["items"].append(item)
                else:
                    monkeys[monkey["case_false"]]["items"].append(item)
                monkey["n_inspected"] += 1

    top2 = sorted([m["n_inspected"] for m in monkeys])[-2:]
    return top2[0] * top2[1]


s = time()
monkeys = parse_data()
sol1 = loop_trough(20, lambda x: x // 3, monkeys)
print("sol1: ", sol1)
print(f"time: {time()-s}\n")

s = time()
monkeys = parse_data()
dividable_all = prod([m["test_div"] for m in monkeys])
sol2 = loop_trough(10000, lambda x: x % dividable_all, monkeys)
print("sol2: ", sol2)
print(f"time: {time()-s}")
