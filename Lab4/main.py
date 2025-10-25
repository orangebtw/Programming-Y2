from collections import deque
type Node = list[int, Node, Node] | None


def gen_bin_tree(
    height: int = 4,
    root: int = 4,
    left_leaf=lambda x: x * 4,
    right_leaf=lambda x: x + 1
) -> Node:
    if height < 0:
        return None
    if height == 0:
        return [root, None, None]

    root_node: Node = [root, None, None]
    queue = deque([root_node])
    level = 0
    while queue:
        if len(queue) == 2 ** level:
            level += 1
        if level == height + 1:
            break

        node = queue.popleft()

        node[1] = [left_leaf(node[0]), None, None]
        queue.append(node[1])

        node[2] = [right_leaf(node[0]), None, None]
        queue.append(node[2])
    return root_node


def print_bin_tree(node: Node, indent: int = 0) -> None:
    if node is None:
        return
    value = node[0]
    print_bin_tree(node[1], indent + 3 + len(str(value)))
    print(' ' * indent + '-- ' + str(value))
    print_bin_tree(node[2], indent + 3 + len(str(value)))


if __name__ == "__main__":
    print_bin_tree(gen_bin_tree())
