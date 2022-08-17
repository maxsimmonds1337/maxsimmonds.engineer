# importing the required module
import matplotlib.pyplot as plt
import cmath

# get a subplot
#plt.plot.subplots(1,4)

# inital complex number
x = 1
y = 0

origin = complex(0,0)

z = complex(x,y)
i = complex(0,1)

# plot the data
ax = plt.subplot(1,4,1)
plt.arrow(0,0,0.8,0, width = 0.01, head_length = 0.2)
plt.xlim([-1,1])
plt.ylim([-1,1])
ax.set_aspect('equal', adjustable='box')

ax = plt.subplot(1,4,2)
plt.arrow(0,0,0,0.8, width = 0.01, head_length = 0.2)
plt.xlim([-1,1])
plt.ylim([-1,1])
ax.set_aspect('equal', adjustable='box')


ax = plt.subplot(1,4,3)
plt.arrow(0,0,-0.8,0, width = 0.01, head_length = 0.2)
plt.xlim([-1,1])
plt.ylim([-1,1])
ax.set_aspect('equal', adjustable='box')

ax = plt.subplot(1,4,4)
plt.arrow(0,0,0,-0.8, width = 0.01, head_length = 0.2)
plt.xlim([-1,1])
plt.ylim([-1,1])
ax.set_aspect('equal', adjustable='box')

# giving a title to my graph
plt.suptitle('Rotating Phasor')

# function to show the plot
plt.show()
