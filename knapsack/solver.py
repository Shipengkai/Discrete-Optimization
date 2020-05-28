#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
The key is that using two algorithm.

"""
from collections import namedtuple
import sys
sys.setrecursionlimit(900000000)

Item = namedtuple("Item", ['index', 'value', 'weight'])


# branch_it                 slow when v/w are the same.
def branch_it(item_count, capacity, items):
    class Node:
        def __init__(self, value, room, item_index, deep, lchild=None, rchild=None, parent=None):
            self.value = value
            self.room = room
            self.item_index = item_index
            self.lchild = lchild
            self.rchild = rchild
            self.deep = deep
            self.parent = parent

        # 计算某节点的value上限
        def linearValue(self):
            lv = self.value
            remain_deep = self.deep
            remain_room = self.room
            while remain_room > 0 and remain_deep < item_count-1:
                remain_deep += 1
                remain_room -= items[remain_deep][2]
                lv += items[remain_deep][1]
            if remain_room < 0:
                lv -= (-remain_room)*items[remain_deep][1] / \
                    items[remain_deep][2]
            return lv

        # 判断是否最后一个节点
        def isLeaf(self):
            return self.deep == item_count - 1

        def build(self):
            global bound
            global solutionl
            if self.isLeaf():
                if bound < self.value:
                    bound = self.value
                    solutionl = self
                return
            index, v, w = items[self.deep + 1]  # 下一个item
            if self.room >= w:
                lchild = Node(self.value+v, self.room-w, index, self.deep+1)
                if lchild.linearValue() > bound:
                    self.lchild = lchild
                    lchild.parent = self
                    lchild.build()
            rchild = Node(self.value, self.room, index, self.deep+1)
            if rchild.linearValue() > bound:
                self.rchild = rchild
                rchild.parent = self
                rchild.build()
    global bound
    taken = [0]*len(items)
    bound = 0
    global solutionl
    solutionl = None
    # items=[(0,v,w),...,(item_count-1,v,w)]
    items.sort(key=lambda item: item[1]/item[2], reverse=True)
    root = Node(0, capacity, items[0], -1)
    root.build()

    cur = solutionl
    while cur.parent != None:
        if cur.parent.lchild == cur:
            taken[cur.item_index] = 1
        cur = cur.parent
    return bound, taken


# dynamic programming       slow when capacity*item_count is very big.
def dynamic_it(item_count, capacity, items):
    dynamic_table = []
    dynamic_table.append([0]*(capacity+1))
    for i in range(1, item_count+1):
        cur_reverse_column = []
        # whether add items[i-1]; append O(1);
        for k in range(0, capacity+1):
            cur_item = items[i-1]
            cur_item_value = cur_item[1]
            cur_item_weight = cur_item[2]
            value_not_add = dynamic_table[i-1][k]
            value_add = (dynamic_table[i-1][k+cur_item_weight] +
                         cur_item_value) if k+cur_item_weight <= capacity else 0
            cur_value = value_not_add if value_not_add > value_add else value_add
            cur_reverse_column.append(cur_value)
        dynamic_table.append(cur_reverse_column)

    value = dynamic_table[item_count][0]

    k = 0
    taken = [0]*len(items)
    for i in range(0, item_count+1):
        if k >= capacity:
            break
        item_id = item_count - i - 1
        if dynamic_table[item_count-i][k] != dynamic_table[item_count-i-1][k]:
            taken[item_id] = 1
            k += items[item_id][2]
    return value, taken


def solve_it(input_data):

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

    value = 0
    taken = [0]*len(items)

    # import timer is much better.But this is OK.
    if item_count != 200:
        value, taken = branch_it(item_count, capacity, items)
    else:
        value, taken = dynamic_it(item_count, capacity, items)

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
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


# if __name__ == "__main__":
#     file_location = './data/ks_10000_0'.strip()
#     with open(file_location, 'r') as input_data_file:
#         input_data = input_data_file.read()

#         print(solve_it(input_data))
