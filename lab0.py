#! /usr/bin/env python3.4

__author__ = 'Jason Yao'

# Global Imports
import csv
import sys

# Math Plot Imports
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid.axislines import SubplotZero

# Returns a column from a csv file
def getColumn(filename, column):
    read = csv.reader(open(filename), delimiter=",")
    csvList = list(read)
    rows = len(csvList)

    columnValues = []
    for rowValue in range(0, rows):
        columnValues.append(csvList[rowValue][column])
    return columnValues

def convertShit(stringArray):
    floatArray = []
    for i in range(1, len(stringArray)):
        floatArray.append(float(stringArray[i][0]))
    return floatArray

def graphShit(figure, xLabel, yLabel, xData, yData):
    fig = plt.figure(1)
    plt.title(figure,)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

    # Generates the axes
    ax = SubplotZero(fig, 111)
    fig.add_subplot(ax)

    for direction in ["xzero", "yzero"]:
        ax.axis[direction].set_axisline_style("-|>")
        ax.axis[direction].set_visible(True)

    for direction in ["left", "right", "bottom", "top"]:
        ax.axis[direction].set_visible(False)

    # Generates the best fit line & Draws it
    m, b = np.polyfit(xData, yData, 1)

    x = np.linspace(0, 0, len(xData))
    filler = []
    for i in range(0, len(xData)):
        filler.append(0)
    ax.plot(x, filler)
    ax.scatter(xData, yData)
    ax.plot(xData, m*xData + b, '-')
    ax.annotate('Least Squares Line:\n' + 'y = ' + str(m) + 'x +' + str(b), xy=(-10, 14), xytext=(-200, 17),
            arrowprops=dict(facecolor='black', shrink=0.05))

    # Annotates the y-intercept
    yintercept = b
    ax.annotate('Y-intercept:\n' + "(0, " +  str(b) + ")", xy=(0, 14), xytext=(40, 10),
            arrowprops=dict(facecolor='black', shrink=0.05))


    fig.savefig('graph.pdf', bbox_inches='tight')


    #
    #     fig = plt.figure(1)
    #     ax = SubplotZero(fig, 111)
    # fig.add_subplot(ax)
    #
    # for direction in ["xzero", "yzero"]:
    #     ax.axis[direction].set_axisline_style("-|>")
    #     ax.axis[direction].set_visible(True)
    #
    # for direction in ["left", "right", "bottom", "top"]:
    #     ax.axis[direction].set_visible(False)
    #
    # x = np.linspace(-0.5, 1., 100)
    # ax.plot(x, np.sin(x*np.pi))

    plt.show()


    return

# Reads in data from .csv file
def main():
    # Grabs the filename from std input
    filename = sys.argv[1]

    with open(filename, newline='') as csvfile: # Automatically closes file-stream IO
        # Separates out data streams
        measurementNumber = getColumn(filename, 0)
        temperatureCelcius = getColumn(filename, 1)
        pressurePoundsPerInchesSquared = getColumn(filename, 2)
        estimatedUncertaintyInPressure = getColumn(filename, 3)
        T_error = getColumn(filename, 4)

        # Generates the data arrays
        newTemp = []
        newPressure = []
        for i in range(1, len(temperatureCelcius)):
            newTemp.append(float(temperatureCelcius[i]))
        for i in range(1, len(pressurePoundsPerInchesSquared)):
            newPressure.append(float(pressurePoundsPerInchesSquared[i]))

        newPressure = np.array(newPressure)
        newTemp = np.array(newTemp)

        # Graphs shit and outputs it to file
        graphShit("Temperature versus Pressure", "Temperature (c)", "Pressure (lb/in^2)", newTemp, newPressure)





    return

# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    main()