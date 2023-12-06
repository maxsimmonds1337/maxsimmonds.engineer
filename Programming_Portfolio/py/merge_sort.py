def merge(left,right):
    sorted_list = []
    
    p1 = p2 = 0

    # two pointers, as list left and right are already ordered, we can start at the left most end and work through
    # 2,4,1
    # 8,3,0

    while p1 < len(left) and p2 < len(right):
        if left[p1] < right[p2]:
            sorted_list.append(left[p1])
            p1 = p1+1
        elif left[p1] > right[p2]:
            sorted_list.append(right[p2])
            p2 = p2+1 
        else:
            #they're the same, so add them both, order doesn't matter
            sorted_list.append(left[p1])
            sorted_list.append(right[p2])
            p1 = p1 + 1
            p2 = p2 + 1
    
    # if there's still elements in the right list, then all of these are larger than the left list, so add the remaining list
    if p2 != len(right):
        while p2 < len(right):
            sorted_list.append(right[p2])
            p2 = p2 + 1
    if p1 != len(left):
        while p1 < len(left):
            sorted_list.append(left[p1])
            p1 = p1 + 1

    return sorted_list    


def merge_sort(unsorted_list):
    # Algo
    # step 0, split array until atomic
    # step 1, start merging elements from the halves based on size

    list_length = len(unsorted_list)
    if list_length > 1:
        left = unsorted_list[:list_length//2]
        left = merge_sort(left)
        right = unsorted_list[list_length//2:]
        right = merge_sort(right)

        new_array = merge(left, right)

        return new_array
    
    return unsorted_list

if __name__ == "__main__":
    print(f'the answe is: {merge_sort([4,3,2,6,4,5,7,1,9,10])}')
