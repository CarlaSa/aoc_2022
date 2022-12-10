from aocd import get_data, submit

data = get_data(year=2022, day=10).split("\n")

cycle = 0
x = 1
score = 0
cycle_image = ""


def check():
    global cycle, x, score, cycle_image
    signal_strength = cycle * x
    if cycle in range(20, 240, 40):
        score += signal_strength
    lit = len(cycle_image)  % 40  in [x-1 % 40, x %40, x+1% 40]
    cycle_image += "█" if lit else "░"


for instr in data:
    bef, z = instr[0:4], instr[5:]
    if bef == "noop":
        cycle +=1
        check()
    else:
        cycle +=1
        check()
        cycle +=1
        check()
        x += int(z)

print(f"Solution 1: \n{score}\n")
print(f"Solution 2:")
for i in range(6):
    print(cycle_image[i* 40:i*40+40])

#submit(score)