from aocd import get_data, submit
data = get_data(year=2022, day=4)

def get_set(ra):
    ra = ra.split("-")
    return set(range(int(ra[0]), int(ra[1])+1))


data = [[get_set(xx) for xx in x.split(",")] for x in data.split("\n")]

sol1 = 0

for d in data:
    if d[0].issubset(d[1]) or d[1].issubset(d[0]):
        sol1 += 1

sol2 = 0

for d in data:
    if len(d[0] & d[1]) > 0:
        sol2 += 1
# submit(sol2)
# submit(sol2)
