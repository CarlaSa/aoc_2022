from aocd import get_data, submit
from typing import Union
from tqdm import tqdm

data = get_data(year=2022, day=15).split("\n")
# with open("input.txt") as f:
#     data = f.read().split("\n")


class Coordinate:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.__add__(-other)

    def __neg__(self):
        return Coordinate(-self.x, -self.y)

    def __abs__(self):
        return abs(self.x) + abs(self.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __lt__(self, other):
        """only if one dimension same"""
        if self.x == other.x:
            return self.y < other.y
        if self.y == other.y:
            return self.x < other.x
        else:
            return None

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __le__(self, other):
        return self < other or self == other

    def __hash__(self):
        return hash((self.x, self.y))


class Interval:
    def __init__(self, left: Union[Coordinate, int], right: Union[Coordinate, int], y = None):
        assert left < right
        if y is not None:
            assert isinstance(left, int) and isinstance(right, int)
            left = Coordinate(left, y)
            right = Coordinate(right, y)
        self.left = left
        self.right = right

    def __add__(self, other):
        if not isinstance(other, Interval):
            intervals = []
            for o in other:
                i = self + o
                if isinstance(i, Interval):
                    intervals.append(i)
                else:
                    intervals += i
            # try reducing
            def reduce_list(l, i):
                if i >= len(l):
                    return l
                i0 = l[i]
                rest_list = [ll for k, ll in enumerate(l) if k != i]
                for k, el in enumerate(rest_list):
                    i1 = i0 + el
                    if isinstance(i1, Interval):
                        rest_list[k] = i1
                        return rest_list
                return l
            for i in range(len(intervals)):
                intervals = reduce_list(intervals, i)
            #
            # for i in range(len(intervals)):
            #     a = intervals[i]
            #     for j in range(i+1, len(intervals)):
            #         a,b = intervals[i], intervals[j]
            #         if isinstance(a+b, Interval):
            #

            return intervals

        # exclusive
        if self.left <= other.left:
            if self.right >= other.right:
                return self
            if self.right < other.right:
                # does overlab exist?
                if self.right >= other.left + Coordinate(-1, 0):
                    return Interval(self.left, other.right)
                else:
                    return [self, other]
        else:
            return other.__add__(self)

    def __repr__(self):
        return str((self.left, self.right))

    def __len__(self):
        return abs(self.right - self.left)

    def cut(self, other):
        self.left = max(self.left, other.left)
        self.right = min(self.right, other.right)

    def cut_t2(self, n):
        other = Interval(0, n, y = self.left.y)
        self.cut(other)


sensor_beacon_pairs = []
for d in data:
    dd = d.split(" ")
    sens = Coordinate(dd[2][2:-1], dd[3][2:-1])
    beac = Coordinate(dd[8][2:-1], dd[9][2:])
    dist = abs(sens - beac)
    sensor_beacon_pairs.append([sens, beac, dist])


def cannot_contain(sensor, beacon, dist, y, ignore_beacon = True):
    adj_dist = dist - abs(sensor.y -y)
    if adj_dist <= 0:
        return None
    if ignore_beacon or beacon.y != y:
        return Interval(sensor.x - adj_dist, sensor.x + adj_dist, y = y)
    else:
        if beacon.x == sensor.x - adj_dist:
            return Interval(sensor.x - adj_dist +1, sensor.x + adj_dist, y=y)
        else:
            return Interval(sensor.x - adj_dist, sensor.x + adj_dist -1, y=y)

def task1(line = 2000000, boundaries = False, ignore_beacon = False):
    coords = None
    for s, b, d in sensor_beacon_pairs:
        interval =  cannot_contain(s, b, d, line, ignore_beacon= ignore_beacon)
        if boundaries and interval is not None:
            interval.cut_t2(boundaries)
        if coords is None:
            coords = interval
        elif interval is not None:
            coords = interval + coords
        else:
            continue
    if coords is None:
        return 0, None
    elif isinstance(coords, list):
        return sum(len(c) for c in coords), coords
    else:
        return len(coords), coords


def task2(n= 4000000):
    for y in tqdm(range(n, 0, -1)):
        s = task1(y, boundaries=n, ignore_beacon= True)
        if s[0] < n :
            x = sorted(s[1], key = lambda x: x.right.x)[0].right.x +1
            res = x * 4000000 + y
            break
    return res


res1 = task1()[0]
res2 = task2()
print(res1, res2)


