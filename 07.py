from aocd import get_data, submit

data = get_data(year=2022, day=7)

class Tree:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = dict()

    def insert_child(self, child_name, child_value):
        self.children[child_name] = child_value

    def link_child(self, other):
        self.children[other.name] = other

    def size(self):
        size = 0
        for key, ch in self.children.items():
            if isinstance(ch, Tree):
                size += ch.size()
            else:
                size += int(ch)
        return(size)

    def __str__(self, einr=""):
        string = ""
        string += (einr + self.name + ":\n")
        if self.children == {}:
            string += f"{einr}  no children\n"
        else:
            for key, ch in self.children.items():
                if isinstance(ch, Tree):
                    string += ch.__str__(einr = einr + "  ")
                else:
                    string += f"{einr}  {key}: {ch}\n"
        return string


# parse tree
curr = None
for commandline in data.split("$"):
    befehl = commandline[1:3]
    if befehl == "cd":
        rest = commandline.split("\n")[0][4:]
        #new_tree = Tree(name=rest, parent=)
        if rest == "/":# first time
            tree = Tree(name="base", parent=None)
            curr = tree
        elif rest == "..":
            curr = curr.parent
        else:
            other = Tree(name=rest, parent=curr)
            assert other.name in curr.children
            curr.link_child(other)
            curr = other

    if befehl == "ls":
        rest = commandline.split("\n")[1:]
        for line in rest:
            if line == "":
                continue
            a, b = line.split(" ")
            if a == "dir":
                curr.insert_child(b, None)
            else:
                curr.insert_child(b, a)

print(tree)

def task1():
    threshold = 100000
    total = 0
    trees = [tree]
    for tr in trees:
        size = tr.size()
        if size < threshold:
            total += size
        for k,v in tr.children.items():
            if isinstance(v, Tree):
                trees.append(v)
    return total


def task2():
    total_space = 70000000
    needed = 30000000
    free = total_space - tree.size()
    trees = [tree]
    curr = total_space
    for tr in trees:
        size = tr.size()
        if size + free > needed:
            if size < curr:
                curr = size
        for k,v in tr.children.items():
            if isinstance(v, Tree):
                trees.append(v)
    return curr


print(task1())
print(task2())
#submit(task1())
#submit(task2())

