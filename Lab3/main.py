type Node = tuple[int, Node, Node] | None

def left_value(root: int) -> int:
    return root + 2

def right_value(root: int) -> int:
    return root * 3

def gen_bin_tree(height: int, root: int) -> Node:
    if height == 0: return None
    left = gen_bin_tree(height - 1, left_value(root)) 
    right = gen_bin_tree(height - 1, right_value(root))  
    return (root, left, right)

def print_bin_tree(node: Node, indent: int = 0) -> None:
    if node == None: return
    value = node[0]
    print_bin_tree(node[1], indent + 3 + len(str(value)))
    print(' ' * indent + '-- ' + str(value))
    print_bin_tree(node[2], indent + 3 + len(str(value)))

if __name__ == "__main__":
    print_bin_tree(gen_bin_tree(5, 1))
