from aocd import get_data, submit

data = get_data(year=2022, day=5)
crates, instructions = data.split("\n\n")

# print(crates)
lines = [[x[i:i + 4] for i in range(0, len(x), 4)] for x in crates.split("\n")]
lines = [[lines[j][i].strip() for j in range(len(lines[0]) - 1, -1, -1)]
         for i in range(0, len(lines))]
lines_dict = {
    int(ll[0]): [ll[i][1] for i in range(1, len(ll)) if len(ll[i]) > 0] for ll in lines
}


def get_upper_crates(l_d):
    upper = [l_d[i][-1] for i in range(1, 10)]
    return "".join(upper)


def move(number, from_, to_):
    for _ in range(number):
        lines_dict[to_].append(lines_dict[from_].pop())

def move2(number, from_, to_):
    temp = []
    for _ in range(number):
        temp.insert(0, (lines_dict[from_].pop()))
    lines_dict[to_] += temp

for line in instructions.split("\n"):
    l = line.split()
    move2(int(l[1]), int(l[3]), int(l[5]))

#after
print(get_upper_crates(lines_dict))

# print(instructions)
submit(get_upper_crates(lines_dict))

# with move is sol1
# with move2 is sol2