from TreeSet import TreeSet


def natural_order(x, y):
    return x - y
tree = TreeSet(natural_order)
sequence = [-4, 11, 6, 18, -1, 8, 13, 0, 3, 19, -5, 7, 9, 12, 2, 17, 4, 1, 10, -3, 5, 14, 15, 16, -2]
for item in sequence:
    tree.insert(item)
for size, item in zip(reversed(range(len(sequence))), range(-5, 20)):
    tree.remove(item)
print(tree)