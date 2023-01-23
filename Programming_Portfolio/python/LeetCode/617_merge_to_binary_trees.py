
from typing import Optional
from collections import deque

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
def print_nodes(TreeNode):
    if TreeNode:
        print_nodes(TreeNode.left)
        print_nodes(TreeNode.right)
        print(TreeNode.val)

class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        # get a queue
        queue = deque()

        queue.appendleft(root1)
        queue.appendleft(root2)

        while len(queue) != 0:
            tree_1_node = queue.pop()
            tree_2_node = queue.pop()

            print(f"popping tree 1 ({tree_1_node.val}) off the queue")
            print(f"popping tree 2 ({tree_2_node.val}) off the queue")

            if not tree_1_node == None: tree_1_node.val = 0
            if not tree_2_node.val == None: tree_2_node.val = 0

            ans = int(tree_1_node.val)+int(tree_2_node.val)

            print(f"the sum of the two is {ans}")

            print(f"pushing the neighbors")
            if tree_1_node.left != None or tree_2_node.left != None:
                queue.appendleft(tree_1_node.left)
                queue.appendleft(tree_2_node.left)
            print(f"tree 1's neighbors left: {tree_1_node.left} and tree 2 left: {tree_2_node.left}")

            if tree_1_node.right != None or tree_2_node.right != None:
                queue.appendleft(tree_1_node.right)
                queue.appendleft(tree_2_node.right)
                print(f"tree 1's neighbors right: {tree_1_node.right} and tree 2 right: {tree_2_node.right}")



# build the tree for root1
root1 = TreeNode(1)
root1.left = TreeNode(3)
root1.right = TreeNode(2)
root1.left.left = TreeNode(5)

# build the tree for root2
root2 = TreeNode(2)
root2.left = TreeNode(1)
root2.left.right = TreeNode(4)
root2.right = TreeNode(3)
root2.right.right = TreeNode(7)

solution = Solution()

solution.mergeTrees(root1, root2)
