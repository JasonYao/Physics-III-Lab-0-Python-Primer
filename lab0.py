#! /usr/bin/env python3.4

__author__ = 'Jason Yao'

# Global Imports
import sys

# Math Plot Imports
import numpy as np
from matplotlib import pyplot as plt

##
# NOTE: THIS PROGRAM DEPENDS ON STANDARD INPUT: TO RUN, USE THIS COMMAND IN THE TERMINAL:
# python3 lab0.py input.csv # WHERE input.csv is the filename, or the path to the file if not in the same directory
#

# Graphs shit
def graphShit(dataTitle, xLabel, yLabel, xData, yData, tError, uncertainty):
    # Gets every subplot into the same figure
    fig = plt.figure(1, figsize=(14,10))
    plt0 = fig.add_subplot(3,1,1)
    plt1 = fig.add_subplot(3,2,3)
    plt2 = fig.add_subplot(3,2,4)
    plt3 = fig.add_subplot(3,2,5)
    plt4 = fig.add_subplot(3,2,6)

    # Least squares line calculations
    m, b = np.polyfit(xData, yData, 1)
    mNice = "%.2f" % m
    bNice = "%.2f" % b
    linearEquation = "Linear fit: y = " + str(mNice) + "x" + str(bNice)

    # Chi weighted line of best fit calculations
    xShit = xData/(uncertainty * uncertainty)
    yShit = 1/(uncertainty * uncertainty)
    xHat = sum(xShit)/sum(yShit)

    xShit2 = yData/(uncertainty * uncertainty)
    yShit2 = 1/(uncertainty * uncertainty)
    yHat = sum(xShit2)/sum(yShit2)

    beta = sum((xData  - xHat) * yData/(uncertainty**2))/sum((xData - xHat) * (xData/(uncertainty**2)))
    alpha = yHat - beta * xHat

    # Plots data & least squares lines
    #plt.title("Lab 0: Python Primer")
    #plt0.xlabel(xLabel)
    #plt0.ylabel(yLabel)
    plt0.scatter(xData, yData)
    plt0.plot(xData, m*xData + b, 'r-', label=linearEquation) # Plots least squares lines
    plt0.plot(xData, alpha + (beta * xData), label="Chi-squared weighted best fit line")# Plots chi squared line

    # Gets error bars
    plt0.errorbar(xData, yData, fmt='ro', label="data", yerr=tError, xerr=uncertainty, ecolor='black')
    plt0.legend(loc = "upper left")

    # Angular calculations
    w_1 = 2 * np.pi * 5             # rad/sec
    w_2 = 2 * np.pi * 5.2           # rad/sec
    newA = 0.1                      # Rad
    t = np.linspace(0, 25, 1000)    # t-step

    theta_a = newA * np.cos(w_1 * t) + newA * np.cos(w_2 * t)
    theta_b = newA * np.cos(w_1 * t) - newA * np.cos(w_2 * t)

    newTheta_a = 2 * newA * np.cos(((w_2 - w_1)/(2))*t) * np.cos(((w_2 + w_1)/(2))*t)
    newTheta_b = 2 * newA * np.sin(((w_2 - w_1)/(2))*t) * np.sin(((w_2 + w_1)/(2))*t)

    plt1.plot(t, theta_a)
    plt2.plot(t, newTheta_a)
    plt3.plot(t, theta_a, t, newTheta_a)
    plt4.plot(t, theta_b, t, newTheta_b)
    plt.savefig('graphs.pdf', bbox_inches='tight')
    plt.show(1) # Shows the graphs
    return

# Reads in data from .csv file
def main():
    # Grabs the filename from std input
    filename = sys.argv[1]
    SKIPROW = 5

    temperature, pressure, uncertainty, error = np.loadtxt(
        filename, skiprows=SKIPROW, unpack=True, usecols=(1,2,3,4), delimiter=',')

    graphPressure = np.array(pressure)
    graphTemperature = np.array(temperature)
    graphUncertainty = np.array(uncertainty)
    graphError = np.array(error)

    # Graphs shit and outputs it to file
    graphShit(
        "Temperature versus Pressure", "Pressure (lb/in^2)", "Temperature (c)",
        graphPressure, graphTemperature, graphError, graphUncertainty)
    return

# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    main()