from collections import deque

image = [[1,1,1],[1,1,0],[1,0,1]]
sr = 1
sc = 1
color = 2

row_length = len(image[0])
col_length = len(image)

stack = deque() # get a stack
stack.append([sr,sc]) # add the first node

while len(stack) != 0:

    print("currently on the stack: {0}".format(stack))

    [sr,sc] = stack.pop() # get the latest coords

    print("changing colour of {0}".format([sr,sc]))

    image[sr][sc] = color # set the colour
    
    # now get the neighbours
    if sr - 1 >= 0 and image[sr-1][sc] != color: # check to see if its in bounds, and not already visited
        print("adding left to stack, {0}".format(sr-1))
        stack.append([sr - 1, sc])
    if sr + 1 < row_length and image[sr][sc] != color:
        print("adding right to stack, {0}".format(sr+1))
        stack.append([sr + 1, sc])
    if sc + 1 < col_length and image[sr][sc+1] != color: 
        print("adding top to stack, {0}".format(sc+1))
        stack.append([sr, sc + 1])
    if sc - 1 >= 0 and image[sr][sc-1] != color: 
        print("adding bottom to stack, {0}".format(sc-1))
        stack.append([sr, sc - 1])

print(image)