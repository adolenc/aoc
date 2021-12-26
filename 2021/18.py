# https://adventofcode.com/2021/day/18
import sys
from math import floor, ceil
from functools import reduce


input = [line.strip() for line in sys.stdin]


# part 1
# def tracefunc(frame, event, arg, indent=[0]):
#       if event == "call":
#           indent[0] += 2
#           print("-" * indent[0] + ">", frame.f_code.co_name, [frame.f_locals[frame.f_code.co_varnames[i]] for i in range(frame.f_code.co_argcount)])
#       elif event == "return":
#           print("-" * indent[0] + '<', "return", arg)
#           indent[0] -= 2
#       return tracefunc
#
# import sys
# sys.settrace(tracefunc)

class SFNode:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
        self.parent = None

class SFLeaf:
    def __init__(self, value):
        self.value = value
        self.parent = None

def sf_split(a):
    if isinstance(a, SFLeaf):
        if a.value >= 10 and a.parent:
            if a.parent.left == a:
                a.parent.left = SFNode()
                a.parent.left.left = SFLeaf(int(floor(a.value / 2)))
                a.parent.left.right = SFLeaf(int(ceil(a.value / 2)))
                a.parent.left.left.parent = a.parent.left
                a.parent.left.right.parent = a.parent.left
                a.parent.left.parent = a.parent
                return True
            if a.parent.right == a:
                a.parent.right = SFNode()
                a.parent.right.left = SFLeaf(int(floor(a.value / 2)))
                a.parent.right.right = SFLeaf(int(ceil(a.value / 2)))
                a.parent.right.left.parent = a.parent.right
                a.parent.right.right.parent = a.parent.right
                a.parent.right.parent = a.parent
                return True
    else:
        if sf_split(a.left):
            return True
        if sf_split(a.right):
            return True
    return False

def sf_explode(a):
    def leftmost_lvl4_path(a, lvl=0):
        if lvl == 4 and isinstance(a, SFNode): return a
        if isinstance(a, SFLeaf): return None
        if lft_found := leftmost_lvl4_path(a.left, lvl+1): return lft_found
        if rgh_found := leftmost_lvl4_path(a.right, lvl+1): return rgh_found
        return None

    def find_first_left_of(a):
        while a.parent.left == a:
            a = a.parent
            if not a.parent:
                return None
        a = a.parent.left
        while not isinstance(a, SFLeaf):
            a = a.right
        return a

    def find_first_right_of(a):
        while a.parent.right == a:
            a = a.parent
            if not a.parent:
                return None
        a = a.parent.right
        while not isinstance(a, SFLeaf):
            a = a.left
        return a


    found = leftmost_lvl4_path(a)
    if not found:
        return False

    if first_left_of := find_first_left_of(found):
        first_left_of.value += found.left.value

    if first_right_of := find_first_right_of(found):
        first_right_of.value += found.right.value

    if found.parent.left == found:
        found.parent.left = SFLeaf(0)
        found.parent.left.parent = found.parent
    else:
        found.parent.right = SFLeaf(0)
        found.parent.right.parent = found.parent

    return True

def sf_reduce(a):
    while True:
        if sf_explode(a): continue
        if sf_split(a): continue
        return a


def sf_sum(a, b):
    n = SFNode(a, b)
    a.parent = n
    b.parent = n
    return sf_reduce(n)

def sf_magnitude(a):
    if isinstance(a, SFLeaf):
        return a.value
    return 3 * sf_magnitude(a.left) + 2 * sf_magnitude(a.right)

def to_sf_number(str):
    def to_tree(lst, parent):
        if isinstance(lst, list):
            n = SFNode()
            n.left = to_tree(lst[0], n)
            n.right = to_tree(lst[1], n)
            n.parent = parent
            return n
        else:
            n = SFLeaf(lst)
            n.parent = parent
            return n
    return to_tree(eval(str), None)


print(sf_magnitude(reduce(sf_sum, map(to_sf_number, input))))

# part 2
print(max(sf_magnitude(sf_sum(to_sf_number(i), to_sf_number(j))) for i in input for j in input))
