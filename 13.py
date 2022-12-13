from aocd import get_data, submit
from functools import cmp_to_key

data = get_data(year=2022, day=13).split("\n\n")
# with open("input.txt") as f:
#     data = f.read().split("\n\n")
data_task1 = [[eval(dd) for dd in d.split("\n")] for d in data]
data_task2 = [eval(dd) for d in data for dd in d.split("\n")]
data_task2 += [[[2]],[[6]]]

def compare(a,b):
    if isinstance(a, int) and isinstance(b, int):
        if a == b:
            return 0
        elif a < b:
            return -1
        else:
            return 1
    elif isinstance(a, int) and isinstance(b, list):
        return compare([a], b)
    elif isinstance(a, list) and isinstance(b, int):
        return compare(a, [b])
    elif isinstance(a, list) and isinstance(b, list):
        for (aa, bb) in zip(a[:len(b)], b[:len(a)]):
            c = compare(aa, bb)
            if c == 0:
                continue
            else:
                return c
        return compare(len(a), len(b))
    else:
        print(a,b)
        raise ValueError("a und b sind irgendwas anderes?")

def task1():
    res = 0
    for k, x in enumerate(data_task1):
        if compare(x[0], x[1]) < 0:
            res+= k+1
    return res

def task2():
    data_task2.sort(key = cmp_to_key(compare))
    res = 1
    for k, a in enumerate(data_task2):
        if a == [[2]]:
            res *= k +1
        if a == [[6]]:
            res *= k+1
            break
    return res


print(task1())
print(task2())