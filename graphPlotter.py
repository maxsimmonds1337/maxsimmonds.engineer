# importing the required module
from argparse import ArgumentDefaultsHelpFormatter
from inspect import ArgInfo
from click import argument
import matplotlib.pyplot as plt
import cmath
import sys
import os
import subprocess
import uuid
import subprocess

result = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"], stdout=subprocess.PIPE)

graphCmd = []

#changedFiles = os.system("git diff --cached --name-only --diff-filter=ACM")

# check to see if we have anything to do
if result.stdout.decode("utf8") != "":
    #if it's not empty, then lets get the list of paths
    paths = result.stdout.decode("utf8").split("\n")
    # now we need to file only the markdown files

    changes = "" ## this will hold the new file contents, so that we can overwrite the file later
    for path in paths:
        if path[-3:] == ".md":
            #if it's a modified markdown file, then let's check for the tag
            #filename = path.split("/")
            #filename = ''.join(filename[-1:]) # get the file name with extension
            cwd = os.getcwd()
            file = os.path.join(cwd + "/" + path)
            with open(file, 'rt') as pushedFile:
                for line in pushedFile:
                    if line.startswith("```graphPlotter"):
                        cmd = next(pushedFile)
                        line = cmd
                        next(pushedFile) ## this removes the ``` at the end
                        graphCmd.append(cmd)
                    changes = changes + line
    
            pushedFile.close()

    for cmd in graphCmd:

        arguments = cmd.split(" ")
        style = arguments[0]
        # plot the data
        if style == "->":
            ## plots a single arrow on an x/y graph, currently hard coded to a -1 - 1 range

            ## usage :
            ## -> x_start y_start dx dx line_width arrow_head_width
            ## example:
            ## -> 0 0 0.8 0 0.02 0.1

            x1 = float(arguments[1])
            y1 = float(arguments[2])
            deltaX = float(arguments[3])
            deltaY = float(arguments[4])
            width = float(arguments[5])
            header_length = float(arguments[6])

            plt.arrow(x1,y1,deltaX,deltaY, width = width, head_length = header_length)
            plt.xlim([-1,1])
            plt.ylim([-1,1])

        if style == "..":
            ## get the x values, these are a list of numbers

            ## usage :
            ## .. x data_to_plot y data_to_plot t title
            ## example:
            ## .. x 0 1 2 3 y 0 1 2 3 4 t my plot

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

            plt.plot(xData, yData)
            #plt.xlim([-1,1])
            #plt.ylim([-1,1])

        # naming the x axis
        plt.xlabel('x')
        # naming the y axis
        plt.ylabel('y')

        # giving a title to my graph
        title = " ".join(title) ## merge elements together
        plt.title(title)

        # function to show the plot
        imageName = uuid.uuid1().hex

        filepath = os.path.join("./programming/python/images","%s.png" % imageName)
        plt.savefig(filepath)

        link = "![Plotted with graphPlotter!](/programming/python/images/" + imageName + ".png)"  

        fin = open(file, "wt")
        changes = changes.replace(cmd, link)
        change = changes + "## " + cmd.join() ## this writes the command as a comment, so that we don't lose the information
        fin.write(changes)
        fin.close()