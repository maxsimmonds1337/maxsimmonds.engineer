
## adjacent list
from ast import IsNot
from collections import deque
from queue import Empty


graph = {"a": ["b", "c"], "b": ["d"], "c": ["e"], "d": ["f"], "e": [], "f": []}

def depth_first_search_print(graph: dict, source_node: str) -> None:
    stack = deque() ## make a stack, using collections.queue, as this is o(1) time complexity for push and popping
    stack.append(source_node) ## initialise the stack
    while len(stack) != 0:
        ## pop the value of the stack
        current_node = stack.pop()
        print(current_node)
        for neighbour in graph[current_node]:
            ## go to each neighbour and push to the stack
            stack.append(neighbour)
    return None

if __name__ == "__main__":
    depth_first_search_print(graph, "a")

