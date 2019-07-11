items = [[16,2],[19,3],[23,4],[28,5]]
capacity = 7

DP_table = []
selection_array = [0,0,0,0]
j=0

while j <= len(items):
    item_list = []
    weight = 0
    while weight <= capacity:
        if j > 0:
            if weight < items[j-1][1]:
                input_value = DP_table[j-1][weight]
            else:
                input_value = max(DP_table[j-1][weight],(DP_table[j-1][weight-(items[j-1][1])] + items[j-1][0]))
        elif j == 0:
            input_value = 0

        item_list.append(input_value)
        weight = weight+1

    DP_table.append(item_list)
    j = j+1

Value = DP_table[len(items)][capacity]

print(Value)

i = len(items)-1
weight = capacity

while i >= 0:
    if DP_table[i+1][weight] == (DP_table[i][weight - (items[i][1])] + items[i][0]):
        selection_array[i]=1
        weight = weight - items[i][1]
    else:
        selection_array[i-1] = 0

    i=i-1
print(selection_array)
