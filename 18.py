from aocd import get_data, submit
from collections import deque, defaultdict

use_test = False
data = get_data(year=2022, day=18)
with open("input.txt") as f:
    data, use_test = f.read(), True

data = set([tuple(int(x) for x in d.split(",")) for d in data.split("\n")])
neighbors = set()

surface = 0
for d in data:
    sides = 6
    for i in [[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, 1], [0, 0, -1]]:
        n = tuple(d[j] + i[j] for j in range(3))
        if n in data:
            sides -= 1
        else:
            neighbors.add(n)
    surface += sides

if not use_test:
    submit(surface, part="a")
print("Task 1: ", surface)

class outside:
    data_max_i = [max(d[i] for d in data) for i in range(3)]
    data_min_i = [min(d[i] for d in data) for i in range(3)]

    def __init__(self):
        self.nodes = set()

    def definitly_outside(self, x):
        if not all(self.data_min_i[i] < x[i] < self.data_max_i[i] for i in range(3)):
            self.nodes.add(x)
        return x in self.nodes

    def __add__(self, x):
        self.nodes.add(x)

# find interior surface
looked_at = defaultdict(lambda: False)
o = outside()
l = []

for n in neighbors:
    if looked_at[n] or o.definitly_outside(n):
        continue
    print(n)
    trapped_surface = 0
    q = deque([n])
    while len(q) > 0:
        curr = q.popleft()
        if looked_at[curr]:
            continue
        looked_at[curr] = True
        curr_neigh = {curr}
        for i in [[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, 1], [0, 0, -1]]:
            neigh = tuple(int(curr[j]) + i[j] for j in range(3))
            if neigh in data:
                trapped_surface += 1
                l.append(neigh)
                continue
            else:
                curr_neigh.add(neigh)
                q.append(neigh)

            if o.definitly_outside(neigh):
                trapped_surface = 0
                for other_n in curr_neigh: # mark all neighbours as outside
                    o + other_n
                q = []
                break
    surface -= trapped_surface

print("Task 2: ", surface)
# if not use_test:
#     if surface > 0:
#         submit(surface)
