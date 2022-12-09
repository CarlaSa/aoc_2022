from aocd import get_data, submit
import numpy as np

data = get_data(year=2022, day=9).split("\n")

directions = { "R": [0,1], "L": [0,-1], "U": [1, 0], "D": [-1,0]}
is_toaching = lambda x,y: all(abs(x - y) <= 1)

def move(h,t):
    if not is_toaching(h, t):
        if t[0] == h[0]:
            di = h[1] - t[1]
            di = di / abs(di)
            t[1] += di
        elif t[1] == h[1]:
            di = h[0] - t[0]
            di = di / abs(di)
            t[0] += di
        else:
            di = h - t
            di[0] = di[0] / abs(di[0])
            di[1] = di[1] / abs(di[1])
            t += di
    return t

def task(n):
    rope = [np.array([0,0]) for _ in range(n)]
    visited = []
    visited.append(rope[-1].tobytes()) #hashable
    for d in data:
        dir, le = d.split(" ")
        for _ in range(int(le)):
            rope[0] += directions[dir]
            for i in range(1, n):
                rope[i] = move(rope[i-1], rope[i])
            visited.append(rope[-1].tobytes())
    sol = len(set(visited))
    print(sol)
    return sol

sol1 = task(2)
sol2 = task(10)
#submit(sol1)