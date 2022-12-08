from aocd import get_data, submit

data = get_data(year=2022, day=8)
# with open("input.txt", "r") as f:
#     data = f.read()
data = [[int(d) for d in dd] for dd in data.split("\n")]
is_visible = [[False for d in dd] for dd in data]

h, w = len(data), len(data[0])


for i in range(h):
    curr_max = -1
    for j in range(w):
        if data[i][j] > curr_max:
            is_visible[i][j] = True
            curr_max = data[i][j]
    curr_max = -1
    for j in range(w-1, 0, - 1):
        if data[i][j] > curr_max:
            is_visible[i][j] = True
            curr_max = data[i][j]

for j in range(w):
    curr_max = -1
    for i in range(h):
        if data[i][j] > curr_max:
            is_visible[i][j] = True
            curr_max = data[i][j]
    curr_max = -1
    for i in range(h-1, 0, -1):
        if data[i][j] > curr_max:
            is_visible[i][j] = True
            curr_max = data[i][j]

sol1 = sum(sum(i) for i in is_visible)

def scenic_score(i,j, mmax = len(data)):
    if i ==0 or j == 0 or i == mmax or j == mmax:
        return  0
    def get_s(ii_, jj_):
        s = 1
        s_max = max(len(ii_), len(jj_))
        if min(len(ii_), len(jj_)) == 0:
            return 0
        for ii in ii_:
            for jj in jj_:
                if data[i][j] > data[ii][jj]:
                    s += 1
                else:
                    return s
        return s_max
    score = 1
    score *= get_s(list(range(i+1, mmax)),[j])
    score *= get_s(list(range(i - 1,-1, -1)), [j])
    score *= get_s([i], list(range(j+1, mmax)))
    score *= get_s([i], list(range(j-1, -1, -1)))
    return score

ss_max = 0
for i in range(h):
    for j in range(w):
        ss_max = max(ss_max, scenic_score(i,j))
sol2 = ss_max

print(sol1)
print(sol2)