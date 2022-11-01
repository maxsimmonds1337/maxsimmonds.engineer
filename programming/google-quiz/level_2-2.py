Ion Flux Relabeling
#     ===================

#     Oh no! Commander Lambda's latest experiment to improve the efficiency of the LAMBCHOP doomsday device has backfired spectacularly. The Commander had been improving the structure of the ion flux converter tree, but something went terribly wrong and the flux chains exploded. Some of the ion flux converters survived the explosion intact, but others had their position labels blasted off. Commander Lambda is having her henchmen rebuild the ion flux converter tree by hand, but you think you can do it much more quickly -- quickly enough, perhaps, to earn a promotion!

#     Flux chains require perfect binary trees, so Lambda's design arranged the ion flux converters to form one. To label them, Lambda performed a post-order traversal of the tree of converters and labeled each converter with the order of that converter in the traversal, starting at 1. For example, a tree of 7 converters would look like the following:

#     7
#     3   6
#     1 2 4 5

#     Write a function solution(h, q) - where h is the height of the perfect tree of converters and q is a list of positive integers representing different flux converters - which returns a list of integers p where each element in p is the label of the converter that sits on top of the respective converter in q, or -1 if there is no such converter.  For example, solution(3, [1, 4, 7]) would return the converters above the converters at indexes 1, 4, and 7 in a perfect binary tree of height 3, which is [3, 6, -1].

#     The domain of the integer h is 1 <= h <= 30, where h = 1 represents a perfect binary tree containing only the root, h = 2 represents a perfect binary tree with the root and two leaf nodes, h = 3 represents a perfect binary tree with the root, two internal nodes and four leaf nodes (like the example above), and so forth.  The lists q and p contain at least one but no more than 10000 distinct integers, all of which will be between 1 and 2^h-1, inclusive.

#     Languages
#     =========

#     To provide a Java solution, edit Solution.java
#     To provide a Python solution, edit solution.py

#     Test cases
#     ==========
#     Your code should pass the following test cases.
#     Note that it may also be run against hidden test cases not shown here.

#     -- Java cases --
#     Input:
#     Solution.solution(5, {19, 14, 28})
#     Output:
#         21,15,29

#     Input:
#     Solution.solution(3, {7, 3, 5, 1})
#     Output:
#         -1,7,6,3

#     -- Python cases --
#     Input:
#     solution.solution(3, [7, 3, 5, 1])
#     Output:
#         -1,7,6,3

#     Input:
#     solution.solution(5, [19, 14, 28])
#     Output:
#         21,15,29

#     Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.


class Node():
    def __init__(self, value):
        self.left = None
        self.right = None
        self.val = value

def postorder(height, nums):
    if height == 1:
        return Node(nums.pop())
    node = Node(nums.pop())
    # node.root = nums.pop()
    node.right = postorder(height-1, nums)
    node.left = postorder(height-1, nums)
    return node

height = 3
children  = [7, 3, 5, 1]

tree = postorder(height, list(range(1, 2 ** height)))

def print_nodes(tree):
    if tree:
        print_nodes(tree.left)
        print_nodes(tree.right)
        print(tree.val)

def search_tree(prev_node, node, value):
    if node is not None:
        if node.val == value:
            try:
                return prev_node.val
            except:
                return -1
        else:
            prev_node = node
            return search_tree(prev_node, node.left, value) or search_tree(prev_node, node.right, value)
    else:
        return False

ans = []

# print(search_tree(-1, tree, 7))

for child in children:
    ans.append(search_tree(-1, tree, child))

print(ans)