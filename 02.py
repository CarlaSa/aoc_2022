from aocd import get_data, submit
data = get_data(year=2022, day=2)
data = data.split("\n")

def score(s):
    opp = {"A": 1, "B": 2, "C": 3}[s[0]]
    you = {"X": 1, "Y": 2, "Z": 3}[s[2]]
    return you + ((you - opp + 1) % 3) * 3


def score2(s):
    opp = {"A": 1, "B": 2, "C": 3}[s[0]]
    strat = {"X": -1, "Y": 0, "Z": 1}[s[2]]
    you = (opp + strat -1) %3 +1
    return you + ((you - opp + 1) % 3) * 3

#ex = ["A X", "B X", "C Z"]

sol_1 = sum(score(d) for d in data)
sol_2 = sum(score2(d) for d in data)

print(sol_1)
print(sol_2)
# submit(sol_1)
# submit(sol_2)
