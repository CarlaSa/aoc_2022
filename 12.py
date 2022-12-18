from aocd import get_data, submit
from collections import deque

# get data
data = get_data(year=2022, day=12).split("\n")
# with open("input.txt") as f:
#     data = f.read().split("\n")

grid: list[list[str]] = [[d for d in dd] for dd in data]
w, h = len(grid), len(grid[0])
vertices = [i for i in range(h * w)]
is_explored = [False for _ in vertices]
distance = [10 ** 8 for _ in vertices]

start = None
end = None
for i in range(w):
    for j in range(h):
        if grid[i][j] == "S":
            start = (i, j)
            grid[i][j] = "a"
        if grid[i][j] == "E":
            end = (i, j)
            grid[i][j] = "z"
        if start is not None and end is not None:
            break


# utility functions / dicts
grid_translation = {
    (i, j): i + j * w for i in range(w) for j in range(h)
}
vertices_translation = {
    i + j * w: (i, j) for i in range(w) for j in range(h)
}


def get_edges(i, j):
    val, n = grid[i][j], []
    for ii, jj in [(i, j + 1), (i, j - 1), (i - 1, j), (i + 1, j)]:
        if -1 < ii < w and -1 < jj < h:
            val2 = grid[ii][jj]
            # can go down or at most one up
            if ord(val2) < ord(val) + 2:
                n.append((ii, jj))
    return n

# task1
start_v = grid_translation[start]
q = deque([start_v])
distance[start_v] = 0

while len(q)> 0:
    curr = q.popleft()
    if is_explored[curr]:
        continue
    curr_dist = distance[curr]
    neighbors = get_edges(*vertices_translation[curr])
    is_explored[curr] = True
    for n in neighbors:
        n_v = grid_translation[n]
        if not is_explored[n_v]:
            distance[n_v] = min(curr_dist + 1, distance[n_v])
            q.append(n_v)
        if n == end:
            q = []
            break

sol1 = distance[grid_translation[end]]
submit(sol1, year=2022, day=12, part="a")

is_explored = [False for _ in vertices]
start_v = grid_translation[start]
start_points = [(i, j) for i in range(w) for j in range(h) if grid[i][j] == "a"]
q = deque(grid_translation[s] for s in start_points)
distance[start_v] = 0
while len(q) > 0:
    curr = q.popleft()
    if is_explored[curr]:
        continue
    curr_dist = distance[curr]
    neighbors = get_edges(*vertices_translation[curr])
    is_explored[curr] = True
    for n in neighbors:
        n_v = grid_translation[n]
        if grid[n[0]][n[1]] == "a":
            distance[n_v] = 0
        distance[n_v] = min(curr_dist + 1, distance[n_v])
        q.append(n_v)

sol2 = distance[grid_translation[end]]
submit(sol1, year=2022, day=12, part="b")
