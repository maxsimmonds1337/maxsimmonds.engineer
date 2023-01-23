# Gearing Up for Destruction
# ==========================

# As Commander Lambda's personal assistant, you've been assigned the task of configuring the LAMBCHOP doomsday device's axial orientation gears. It should be pretty simple -- just add gears to create the appropriate rotation ratio. But the problem is, due to the layout of the LAMBCHOP and the complicated system of beams and pipes supporting it, the pegs that will support the gears are fixed in place.

# The LAMBCHOP's engineers have given you lists identifying the placement of groups of pegs along various support beams. You need to place a gear on each peg (otherwise the gears will collide with unoccupied pegs). The engineers have plenty of gears in all different sizes stocked up, so you can choose gears of any size, from a radius of 1 on up. Your goal is to build a system where the last gear rotates at twice the rate (in revolutions per minute, or rpm) of the first gear, no matter the direction. Each gear (except the last) touches and turns the gear on the next peg to the right.

# Given a list of distinct positive integers named pegs representing the location of each peg along the support beam, write a function solution(pegs) which, if there is a solution, returns a list of two positive integers a and b representing the numerator and denominator of the first gear's radius in its simplest form in order to achieve the goal above, such that radius = a/b. The ratio a/b should be greater than or equal to 1. Not all support configurations will necessarily be capable of creating the proper rotation ratio, so if the task is impossible, the function solution(pegs) should return the list [-1, -1].

# For example, if the pegs are placed at [4, 30, 50], then the first gear could have a radius of 12, the second gear could have a radius of 14, and the last one a radius of 6. Thus, the last gear would rotate twice as fast as the first one. In this case, pegs would be [4, 30, 50] and solution(pegs) should return [12, 1].

# The list pegs will be given sorted in ascending order and will contain at least 2 and no more than 20 distinct positive integers, all between 1 and 10000 inclusive.

pegs = [50, 50, 50]
lengths = [] 
gear_sizes = []

from fractions import Fraction

# step 0, calculate the lenths. There will be pegs.length - 1 lengths

num_of_pegs = len(pegs)-1

for i in range(0, num_of_pegs):
    lengths.append(pegs[i + 1] - pegs[i])

result = lengths[0]

for i in range (1, len(lengths)):
    result = result - (lengths[i])

result = float(result) / 0.5
gear_sizes.append(result)

for i in range(1, num_of_pegs):
    result = lengths[i]
    for j in range(i, len(lengths)-1):
        result = result - (lengths[j])
    gear_sizes.append(result-(gear_sizes[0]/2))
gear_sizes.append(gear_sizes[0]/2)

for gear_size in gear_sizes:
    if gear_size < 1:
        print([-1,-1])

for (gear_size, i) in zip(gear_sizes, lengths):
    if gear_size > i:
        
        print([-1,-1])

print(gear_sizes[0])

a = Fraction(gear_sizes[0]).limit_denominator()

print([a.numerator, a.denominator])