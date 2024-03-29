#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    weight = 0
    taken = [0]*len(items)

    #for item in items:
       # if weight + item.weight <= capacity:
           # taken[item.index] = 1
           # value += item.value
           # weight += item.weight



    DP_table = []
    DP_coloumn = []
    wt = 0
    while wt <= capacity:
        DP_coloumn.append(0)
        wt=wt+1
    DP_table.append(DP_coloumn)

    for item in items:
        DP_coloumn = []
        wt = 0
        while wt <= capacity:
            if wt < item.weight:
                input_value = DP_table[item.index][wt]
            else:
                input_value = max(DP_table[item.index][wt],(DP_table[item.index][wt-(item.weight)] + item.value))
            DP_coloumn.append(input_value)
            wt = wt+1

        DP_table.append(DP_coloumn)

    value = DP_table[len(items)][capacity]
    items = items[::-1]
    wt = capacity

    for item in items:
        if DP_table[(item.index)+1][wt] == (DP_table[item.index][wt - (item.weight)] + item.value):
            taken[item.index] = 1
            wt = wt - item.weight


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
