# importing the required module
from email.base64mime import header_length
import matplotlib.pyplot as plt
import cmath
import sys

x1 = float(sys.argv[1])
x2 = float(sys.argv[2])
y1 = float(sys.argv[3])
y2 = float(sys.argv[4])

style = sys.argv[5]

# plot the data
if style == "->":
    width = float(sys.argv[6])
    header_length = float(sys.argv[7])

    plt.arrow(x1,y1,x2,y2, width = width, head_length = header_length)
    plt.xlim([-1,1])
    plt.ylim([-1,1])

# naming the x axis
plt.xlabel('x')
# naming the y axis
plt.ylabel('y')

# giving a title to my graph
plt.title('Rotating Phasor')

# function to show the plot
plt.show()
