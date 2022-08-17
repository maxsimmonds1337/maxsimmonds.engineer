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

for j in range(1,5):
    # plot the data
    plt.subplot(1,4,j)
    plt.plot([z])

    # naming the x axis
    plt.xlabel('x')
    # naming the y axis
    plt.ylabel('y')

    # giving a title to my graph
    plt.title('Rotating Phasor')

    z = z*i ## rotate the phasor


# function to show the plot
plt.show()
