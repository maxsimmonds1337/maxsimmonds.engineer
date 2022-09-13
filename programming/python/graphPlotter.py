# importing the required module
from email.base64mime import header_length
import matplotlib.pyplot as plt
import cmath
import sys
import os
import subprocess
import uuid
import subprocess

##run a git command, check for diffs between the current space and the last commit. --cached is the stages commits, name-only will give the paths, diff filter with ACM
## shows only added, copied, and modified files
result = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"], stdout=subprocess.PIPE)


# check to see if we have anything to do
if result.stdout.decode("utf8") != "":
    #if it's not empty, then lets get the list of paths
    paths = result.stdout.decode("utf8").split("\n")
    # now we need to file only the markdown files
    for path in paths:
        if path[-3:] == ".md":
            #if it's a modified markdown file, then let's check for the tag
            with open(path, 'w') as pushedFile:
                for line in pushedFile:
                    if line.startswith("```graphPlotter"):
                        graphCmd = next(pushedFile)
                        filename = uuid.uuid1().hex
                        filepath = os.path.join("/programming\python\images","%s.png" % filename)
                        line.replace("![Plotted with graphPlotter!](" + filepath + ")") # replace the current line with the link to the picture
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
    plt.savefig(filepath)
