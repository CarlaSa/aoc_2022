from aocd import get_data, submit
data = get_data(year=2022, day=3)

def priority(s):
    if s.islower():
        return ord(s) - ord("a") + 1
    else:
        return ord(s) - ord("A") + 27

#data = "vJrwpWtwJgWrhcsFMMfFFhFp\njqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL\nPmmdzqPrVvPwwTWBwg\nwMqvLMZHhHMvwLHjbvcjnnSBnvTQFn\nttgJtRGJQctTZtZT\nCrZsJsPPZsGzwwsLwLmpwMDw"
sum_ = 0
for backpack in data.split("\n"):
    l = len(backpack)
    comp1, comp2 = backpack[0:l // 2], backpack[l//2: ]
    assert len(comp1) == len(comp2)
    same_item = list(set([item for item in comp1 if item in comp2]))[0]
    pr = priority(same_item)
    sum_ += pr
print(sum_)


data = data.split("\n")
sum_ = 0
for i in range(len(data) // 3 ):
    group = [data[3*i + j] for j in range(3)]
    same_item = set(i for i in group[0]) & set(i for i in group[1]) & set(i for i in group[2])
    sum_ += priority(list(same_item)[0])
print(sum_)

submit(sum_)
#submit(sol2)
