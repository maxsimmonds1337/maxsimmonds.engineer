import matplotlib.pyplot as plt

cmd = ".. x 0 1 2 3 4 y 1 0 -1 0 1 t Imaginary vs Time"

arguments = cmd.split(" ")

xStart = arguments.index("x") + 1   ## get the position of the first x value
xEnd = arguments.index("y") - 1     ## get the position of the last x value

yStart = arguments.index("y") + 1   ## get the position of the first x value
yEnd = arguments.index("t") - 1          ## get the position of the last y value

title = arguments.index("t") + 1
title = arguments[title:]           ## this gets the plot name, allowing for spaces. This only works if the plot name is the last thing in the command

## call the plt.plot() function

xData = arguments[xStart:xEnd]
xData = [float(i) for i in xData]
yData = arguments[yStart:yEnd]
yData = [float(i) for i in yData]


print(xData)
print(yData)

plt.plot(xData, yData)
plt.show()