type Node = tuple[int, Node, Node] | None

def gen_bin_tree(
    height: int,
    root: int,
    left_leaf = lambda x: x * 4,
    right_leaf = lambda x: x + 1
) -> Node:
    if height == 0: return None
    left = gen_bin_tree(height - 1, left_leaf(root), left_leaf, right_leaf) 
    right = gen_bin_tree(height - 1, right_leaf(root), left_leaf, right_leaf) 
    return (root, left, right)

def print_bin_tree(node: Node, indent: int = 0) -> None:
    if node == None: return
    value = node[0]
    print_bin_tree(node[1], indent + 3 + len(str(value)))
    print(' ' * indent + '-- ' + str(value))
    print_bin_tree(node[2], indent + 3 + len(str(value)))

if __name__ == "__main__":
    print_bin_tree(gen_bin_tree(4, 4))
