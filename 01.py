from aocd import get_data, submit

data = get_data(year=2022, day=1)
cals = [sum(int(i) for i in d.split("\n")) for d in data.split("\n\n")]
sol1 = max(cals)
sol2 = sum(sorted(cals)[-3:])

# submit(sol1)
submit(sol2)
