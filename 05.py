from aocd import get_data, submit
import pandas as pd
from io import StringIO
from copy import deepcopy

data = get_data(year=2022, day=5)
crates, instructions = data.split("\n\n")

# first idea
lines = [[x[i:i + 4] for i in range(0, len(x), 4)] for x in crates.split("\n")]
lines = [[lines[j][i].strip() for j in range(len(lines[0]) - 1, -1, -1)]
         for i in range(0, len(lines))]
lines_dict = {
    int(ll[0]): [ll[i][1] for i in range(1, len(ll)) if len(ll[i]) > 0] for ll in lines
}

# second method using pandas
d = pd.read_fwf(StringIO(crates), header = None)
d = d.rename(columns=d.iloc[8]).drop(index = 8).reset_index(drop=True) # last row to column
d = d.applymap(lambda x: x.strip("[] "), na_action = "ignore") # remove brackets
d = d.reindex(index=d.index[::-1]) # turn around
lines_dict_alt = {int(k): [y for y in d[k].to_list() if not pd.isna(y)] for k in d.columns}


def get_upper_crates(l_d):
    """get the correct output from moved crates (the uppermost crates from left to right)"""
    upper = [l_d[i][-1] for i in range(1, 10)]
    return "".join(upper)


def task1(l_dict):
    """task 1"""
    def move(number, from_, to_):
        for _ in range(number):
            l_dict[to_].append(l_dict[from_].pop())
    for line in instructions.split("\n"):
        l = line.split()
        move(int(l[1]), int(l[3]), int(l[5]))
    return l_dict


def task2(l_dict):
    """task 2"""
    def move(number, from_, to_):
        temp = []
        for _ in range(number):
            temp.insert(0, (l_dict[from_].pop()))
        l_dict[to_] += temp
    for line in instructions.split("\n"):
        l = line.split()
        move(int(l[1]), int(l[3]), int(l[5]))
    return l_dict

sol1 = get_upper_crates(task1(deepcopy(lines_dict)))
sol2 = get_upper_crates(task2(deepcopy(lines_dict)))

print(sol1)
print(sol2)

#submit(sol1)
#submit(sol2
