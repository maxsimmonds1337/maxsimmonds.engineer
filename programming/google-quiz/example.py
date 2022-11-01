from typing import Optional, List
import sys


class Node():
    value: int
    left: Optional["Node"]
    right: Optional["Node"]

    def __init__(self, value: int):
        self.value = value
        self.left = None
        self.right = None

    def __str__(self) -> str:
        coalesce = lambda x: x if x is not None else "ø"
        return f"( <{self.value}> => {{ {coalesce(self.left)} , {coalesce(self.right)} }} )"


def build_tree(levels: int) -> Optional[Node]:
    if levels <= 0:
        return None

    count = 0

    count += 1
    root = Node(count)

    prev = [root]

    for _ in range(1, levels):
        current = []
        for parent in prev:
            count += 1
            left = Node(count)
            count += 1
            right = Node(count)
            current += [left, right]
            parent.left = left
            parent.right = right
        prev = current
    return root


def print_tree(root: Optional[Node]) -> None:
    if root is None:
        print("(no tree generated)")
        return
    print(root)


def main(argv: List[str]) -> None:
    levels = int(argv[0])
    tree = build_tree(levels)
    print_tree(tree)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Arguments: <levels>")
    main(sys.argv[1:])
