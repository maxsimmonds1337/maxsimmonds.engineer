``` python
# The isBadVersion API is already defined for you.
# @param version, an integer
# @return an integer
# def isBadVersion(version):

class Solution:
    
    def firstBadVersion(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        ## we want the first bad, so true means we need to go right, bad is left.
        ## stop condition is when we find a good next to a bad,

        ## start at n/2, make call
        ## if false
            ## check if left neighbour is true, if yes, return index
            ## else, search left half
        ## else
            ## check if right neighbour is true, if yes, return index + 1
            ## else, search right half
        
        start = 0
        stop = n
        
        while start <= stop: ## not sure what to so here yet, but will sort that out later
            mid_point = int((start+stop)/2)

            if isBadVersion(mid_point):
                #this means we've hit a bad version, lets check if it's neighbour on the left is false, is so, this is the first bad version
                if not isBadVersion(mid_point-1):
                    return mid_point
                else:
                    ## we eed to search left, so re shift the pointers
                    stop = mid_point-2
            else:
                ## if we're here, then we hit a false, so the bad version is somewhere on the right
                if isBadVersion(mid_point+1): # we check it's neighbour, to see if it's the first bad version
                    # if it is, we reutn this
                    return mid_point+1
                else:
                    start = mid_point + 2
```