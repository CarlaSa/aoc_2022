from aocd import get_data, submit

data = get_data(year=2022, day=6)


def process_message(n):
    for i in range(n, len(data) +1):
        slice = data[i-n:i]
        if len(list(set(slice))) == n:
            return(i)

sol1 = process_message(4)
sol2 = process_message(14)
print(sol1, sol2)

#submit(sol1)

