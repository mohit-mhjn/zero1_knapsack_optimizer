#!/usr/bin/python
# -*- coding: utf-8 -*-

#from collections import namedtuple
#Item = namedtuple("Item", ['index', 'value', 'weight'])
def lin_relax(cap,depth):
    global items, item_count
    for i in items:
        i.append(round((i[1])/(i[2]),3))
    left_over = cap
    opt_eval = 0
    while left_over > 0 and depth < item_count:
        k = -1
        max_at = 0
        for j in range(depth, item_count):
            if (items[j][3]) > k:
                k = items[j][3]
                max_at = j
        if left_over >= items[max_at][2]:
            opt_eval = opt_eval + items[max_at][1]
            left_over = left_over - items[max_at][2]
        else:
            opt_eval = opt_eval + left_over*(items[max_at][3])
            left_over = 0
        items[max_at][3] = 0
        del k
        del max_at
    for i in items:
        del i[3]
    del left_over
    return opt_eval             # Optimalistic Eval

class Node(object):
    parent = None
    left_child = None       #not selecting
    right_child = None      #selecting
    attribute = None
    def __init__(self, room, upper_bound, value, depth):
        self.upper_bound = upper_bound
        self.room = room
        self.value = value
        self.depth = depth
    def __repr__(self):
        return str([self.upper_bound, self.room, self.value, self.depth])

def left_branch(obj):       #left Node is not selecting
    global items
    left_value = obj.value
    left_room = obj.room
    temp = items[obj.depth][2]
    items[obj.depth][2] = 10**10
    left_depth = obj.depth+1
    left_upper_bound = left_value + lin_relax(left_room,left_depth)
    items[obj.depth][2] = temp
    del temp
    left_child = Node(left_room,left_upper_bound,left_value,left_depth)
    left_child.parent = obj
    left_child.attribute = 0
    obj.left_child = left_child
    return left_child

def right_branch(obj):      #right Node is selecting
    global items
    right_value = obj.value + items[obj.depth][1]
    right_room = obj.room - items[obj.depth][2]
    right_upper_bound = obj.upper_bound
    right_depth = obj.depth+1
    right_child = Node(right_room,right_upper_bound,right_value,right_depth)
    right_child.parent = obj
    right_child.attribute = 1
    obj.right_child = right_child
    return right_child

def depth_first(obj):
    global node_stack, items, item_count, current_best, taken
    node_stack.append(obj)
    while node_stack:
        current = node_stack.pop()
        while current.depth < len (items) and current.upper_bound > current_best.value:
            if right_branch(current).room >= 0:
                node_stack.append(left_branch(current))
                current = right_branch(current)
            else:
                current = left_branch(current)
        if current.value > current_best.value:
            current_best = current
    return current_best

def back_track(obj):
    global items,taken
    while True:
        taken[items[obj.depth-1][0]] = obj.attribute
        obj = obj.parent
        if obj.depth == 0:
            break
    return None

def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    global items,item_count,capacity,taken,node_stack,current_best
    lines = input_data.split('\n')
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    items = []
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append([i-1,int(parts[0]),int(parts[1])])

    items = sorted(items, key=lambda tup: tup[1]/tup[2])
    items = items[::-1]
    taken = [0]*len(items)
#***************************************************************
    node_stack = []
    root_Node = Node(capacity,lin_relax(capacity,0),0, 0)
    current_best = Node(0,0,0,0)
    solution = depth_first(root_Node)
    value = solution.value
    back_track(solution)

#****************************************************************
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
