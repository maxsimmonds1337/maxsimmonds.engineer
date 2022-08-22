# importing the required module
from email.base64mime import header_length
import matplotlib.pyplot as plt
import cmath
import sys
import os
import subprocess
import uuid
import subprocess

result = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"], stdout=subprocess.PIPE)

#changedFiles = os.system("git diff --cached --name-only --diff-filter=ACM")

# check to see if we have anything to do
if result.stdout != 0:
    #if it's not empty, then lets get the list of paths
    paths = result.stdout.decode("utf8").split("\n")
    # now we need to file only the markdown files
    for path in paths:
        if path[-3:] == ".md":
            #if it's a modified markdown file, then let's check for the tag
            with open(path, 'r+') as pushedFile:
                for line in pushedFile:
                    if line.startswith("```graphPlotter"):
                        graphCmd = next(pushedFile)
                        break

arguments = graphCmd.split(" ")
x1 = float(arguments[0])
y1 = float(arguments[1])
deltaX = float(arguments[2])
deltaY = float(arguments[3])

style = arguments[4]

# plot the data
if style == "->":
    width = float(arguments[5])
    header_length = float(arguments[6])

    plt.arrow(x1,y1,deltaX,deltaY, width = width, head_length = header_length)
    plt.xlim([-1,1])
    plt.ylim([-1,1])

# naming the x axis
plt.xlabel('x')
# naming the y axis
plt.ylabel('y')

# giving a title to my graph
plt.title('Rotating Phasor')

# function to show the plot
filename = uuid.uuid1().hex
filepath = os.path.join("programming\python\images","%s.png" % filename)
plt.savefig(filepath)
