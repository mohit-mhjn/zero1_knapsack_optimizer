items = [[16,2,0],[19,3,0],[23,4,0],[28,5,0],[16,2,0],[19,3,0],[23,4,0],[28,5,0],[16,2,0],[19,3,0],[23,4,0],[28,5,0],[16,2,0],[19,3,0],[23,4,0],[28,5,0],[16,2,0],[19,3,0],[23,4,0],[28,5,0]]
capacity = 70



def lin_relax(capacity,depth):
    global items
    for i in items:
        i.append(round((i[0])/(i[1]),3))
    left_over = capacity
    opt_eval = 0
    while left_over > 0 and depth < len(items):
        k = -1
        max_at = 0
        for i in range(depth, len(items)):
            if items[i][3] > k:
                k = items[i][3]
                max_at = i
        if left_over >= items[max_at][1]:
            opt_eval = opt_eval + items[max_at][0]
            left_over = left_over - items[max_at][1]
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
    temp = items[obj.depth][1]
    items[obj.depth][1] = 10**10
    left_depth = obj.depth+1
    left_upper_bound = left_value + lin_relax(left_room,left_depth)
    items[obj.depth][1] = temp
    del temp
    #items[obj.depth][2] = 0
    left_child = Node(left_room,left_upper_bound,left_value,left_depth)
    left_child.parent = obj
    obj.left_child = left_child
    return left_child

def right_branch(obj):      #right Node is selecting
    global items
    right_value = obj.value + items[obj.depth][0]
    #items[obj.depth][2] = 1
    right_room = obj.room - items[obj.depth][1]
    right_upper_bound = obj.upper_bound
    right_depth = obj.depth+1
    right_child = Node(right_room,right_upper_bound,right_value,right_depth)
    right_child.parent = obj
    obj.right_child = right_child
    return right_child


root_Node = Node(capacity, lin_relax(capacity,0),0, 0)
#print (right_branch(left_branch(right_branch(root_Node))))
#print (right_branch(right_branch(root_Node)))
#print (left_branch(root_Node))
node_stack = []
current_best = Node(0,0,0,0)

def depth_first(obj):
    global node_stack
    global items
    global current_best
    if obj.room == 0:
        global current_best_opt_eval
        if obj.value > current_best.value:   #updating best opt eval
            current_best = obj
        return obj
            #print ("updated best")
    while obj.depth < len(items):
        x = right_branch(obj)
        y = left_branch(obj)
        if x.room >= 0:
            #print ("selected ",x)  #obj is taken
            #print ("appended in stack",y)
            node_stack.append(y)
            items[obj.depth][2]=1       #item taken
            return depth_first(x)
        else:
            #print ("rejected", x)     #obj is rejected
            #print ("processing", y)
            items[obj.depth][2]=0       #item taken
            return depth_first(y)
    return obj


def back_track(obj):
    global items,taken
    while True:
        taken[items[obj.depth-1][0]] = obj.attribute
        obj = obj.parent
        if obj.depth == 0:
            break
    return None

back_track(depth_first(root_Node))
print (current_best)
print (items)

#xx=right_branch(left_branch(left_branch(right_branch(root_Node))))
#print (xx.upper_bound)
