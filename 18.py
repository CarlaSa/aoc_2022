from aocd import get_data, submit
from collections import deque, defaultdict

# data
use_test = False
data = get_data(year=2022, day=18)
# with open("input.txt") as f:
#     data, use_test = f.read(), True
data = set([tuple(int(x) for x in d.split(",")) for d in data.split("\n")])

# task 1
neighbors = set()
surface = 0
for d in data:
    sides = 6
    for i in [[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, 1], [0, 0, -1]]:
        n = tuple(d[j] + i[j] for j in range(3))
        if n not in data:
            surface += 1
            neighbors.add(n) #for task 2

# solution 1
if not use_test:
    submit(surface, part="a")
print("Task 1: ", surface)


class Outside:
    data_max_i = [max(d[i] for d in data) for i in range(3)]
    data_min_i = [min(d[i] for d in data) for i in range(3)]
    nodes = set()

    def definitely_outside(self, x):
        if not all(self.data_min_i[i] < x[i] < self.data_max_i[i] for i in range(3)):
            self.nodes.add(x)
        return x in self.nodes

    def add(self, x):
        self.nodes.add(x)




# find interior surface
looked_at = defaultdict(lambda: False)
outside = Outside()

for starting_neighbour in neighbors:
    if looked_at[starting_neighbour]:
        continue
    trapped_surface = 0
    q = deque([starting_neighbour])
    neighborhood = {starting_neighbour}
    while len(q) > 0:
        curr = q.popleft()
        if looked_at[curr]:
            continue
        looked_at[curr] = True
        for i in [[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, 1], [0, 0, -1]]:
            neigh = tuple(int(curr[j]) + i[j] for j in range(3))
            if neigh in data:
                trapped_surface += 1
                continue
            else:
                neighborhood.add(neigh)
                q.append(neigh)

            if outside.definitely_outside(neigh):
                trapped_surface = 0
                for other_n in neighborhood: # mark all neighbours as outside
                    outside.add(other_n)
                q = []
                break
    surface -= trapped_surface

# sol 2
if not use_test:
    submit(surface, part="b")
print("Task 2: ", surface)