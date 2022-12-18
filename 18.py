from aocd import get_data, submit
from collections import deque, defaultdict

use_test = False
data = get_data(year=2022, day=18)
# with open("input.txt") as f:
#     data, use_test = f.read(), True

data_set = set(data.split("\n"))  # for lookup
data = [[int(x) for x in d.split(",")] for d in data.split("\n")]
neighbors = set()

surface = 0
for d in data:
    sides = 6
    for i in [[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, 1], [0, 0, -1]]:
        n = [d[j] + i[j] for j in range(3)]
        n_str = ",".join(str(nn) for nn in n)
        if n_str in data_set:
            sides -= 1
        else:
            neighbors.add(n_str)

    surface += sides

submit(surface, part="a")
print("Task 1: ", surface)

data_max_i = [max(d[i] for d in data) for i in range(3)]
data_min_i = [min(d[i] for d in data) for i in range(3)]
def definitly_outside(x):
    return not all(data_min_i[i] - 1 < x[i] < data_max_i[i] + 1 for i in range(3))


# find interior surface
# looked_at = {n: False for n in neighbors}
looked_at = defaultdict(lambda: False)
outside = set()

for n in neighbors:
    if looked_at[n]:
        continue
    trapped_surface = 0
    q = deque([n])
    while len(q) > 0:
        curr = q.popleft()
        if looked_at[curr]:
            continue
        else:
            looked_at[curr] = True
        curr_list = curr.split(",")
        for i in [[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, 1], [0, 0, -1]]:
            n_n = [int(curr_list[j]) + i[j] for j in range(3)]
            n_n_str = ",".join(str(nn) for nn in n_n)
            if n_n_str in data_set:
                trapped_surface += 1
            elif n_n_str in outside:
                outside.add(curr)
                looked_at[n_n_str] = True
                trapped_surface = 0
                # q = []
                # break
            else:
                if looked_at[n_n_str]:
                    continue
                else:
                    if definitly_outside(n_n):
                        outside.add(n_n_str)
                        looked_at[n_n_str] = True
                        trapped_surface = 0
                        q = []
                        break
                    else:
                        q.append(n_n_str)
    surface -= trapped_surface

print("Task 2: ", surface)
# if not use_test:
#     if surface > 0:
#         submit(surface)


# for n in neighbors:
#     if looked_at[n]:
#         continue
#     trapped_surface = 0
#     is_trapped = True
#     q = deque([n])
#     unknown = 0
#     while len(q) > 0:
#         curr = q.popleft()
#         if looked_at[curr]:
#             continue
#         else:
#             looked_at[curr] = True
#         curr_list = curr.split(",")
#         for i in [[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, 1], [0, 0, -1]]:
#             n_n = [int(curr_list[j]) + i[j] for j in range(3)]
#             n_n_str = ",".join(str(nn) for nn in n_n)
#             if n_n_str in data_set:
#                 trapped_surface += 1
#
#             elif n_n_str in outside:
#                 outside.add(curr)
#                 looked_at[n_n_str] = True
#                 is_trapped = False
#                 q = []
#                 break
#             # elif n_n_str in neighbors:
#             #     if not looked_at[n_n_str]:
#             #         q.append(n_n_str)
#             else:
#                 if looked_at[n_n_str]:
#                     continue
#                 else:
#                     if definitly_outside(n_n):
#                         outside.add(n_n_str)
#                         looked_at[n_n_str] = True
#                         is_trapped = False
#                         q = []
#                         break
#                     else:
#                         q.append(n_n_str)
#                 # if n_n_str in looked_at:
#                 #     continue
#                 # else:
#                 #     looked_at[n_n_str] = False
#                 #     if definitly_outside(n_n):
#                 #         looked_at[n_n_str] = True
#                 #         is_trapped = False
#                 #         q = []
#                 #         break
#                 #     else:
#                 #         unknown += 1
#                 #         q.append(n_n_str)
#                 # is_trapped = False
#                 # q = []
#                 # break
#         # if unknown > 45:
#         #     is_trapped = False
#         #     q = []
#         #     break
#     if is_trapped:
#         surface -= trapped_surface