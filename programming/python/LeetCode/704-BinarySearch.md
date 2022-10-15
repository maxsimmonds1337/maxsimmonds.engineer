```python
class Solution(object):
    def search(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """

        nums_length = len(nums) # this doens't change

        def mysearch(nums, target, left, right):

            while (left <= right):
                nums_mid = (left+right)//2
                if(nums[nums_mid] == target):
                    return nums_mid
                elif nums[nums_mid] > target:
                    right = nums_mid - 1
                    mysearch(nums, target, left, right)
                else:
                    left = nums_mid + 1
                    mysearch(nums, target, left, right)
            return -1

        return mysearch(nums, target, 0, len(nums)-1)
```