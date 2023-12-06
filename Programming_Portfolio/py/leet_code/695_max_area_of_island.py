
from collections import deque


def dfs(grid, row, col, count):

    if not(0 <= row < len(grid) and 0<= col < len(grid[0])) or grid[row][col] != 1:
        return count
    else:
        count = count + 1 # if we're here, then the cell is one, and we need to increase the counter
        grid[row][col] = 2 # so we don't go over it again, this is making the cell "visitied"

        # check all four neighbours
        count = dfs(grid, row, col+1, count)
        count = dfs(grid, row, col-1, count)
        count = dfs(grid, row-1, col, count)
        count = dfs(grid, row+1, col, count)

    return count

def maxAreaOfIsland(grid) -> int:
    max_count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                count = 0
                count = dfs(grid, i, j, count)
                if count > max_count: max_count = count
    return max_count

grid = [[1,1,1,0,0,0,0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0,1,1,1,0,0,0],
        [0,1,1,0,1,0,0,0,0,0,0,0,0],
        [0,1,0,0,1,1,0,0,1,0,1,0,0],
        [0,1,0,0,1,1,0,0,1,1,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,0,0,0]]

print(maxAreaOfIsland(grid))
print(grid)


# [[2, 2, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
#  [0, 2, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0],
#  [0, 2, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
#  [0, 2, 0, 0, 2, 2, 0, 0, 2, 0, 2, 0, 0],
#  [0, 2, 0, 0, 2, 2, 0, 0, 2, 2, 2, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0]]