# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import math

class Cboundary:
    def __init__(self, c0, c1, c2, c3, startX, endX):
        self.c0 = c0
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.startX = startX
        self.endX = endX
        
    def draw_polynomial(self, ax, boundarycolor='orange', linewidth=1):
        x = np.linspace(self.startX, self.endX, 100)  # Sample data.
        y = [self.c0  + self.c1 * _x + 1.0/2.0*self.c2 * math.pow(_x, 2) + 1.0/6.0*self.c3 * math.pow(_x, 3) for _x in x]
        ax.plot(x, y, color=boundarycolor, linewidth=linewidth);  # Plot some data on the axes.
        
    
def setaxsproperties(axs):
    axs.axis([0, 70, -10, 10])
    axs.set_aspect('equal', adjustable='datalim')
    axs.grid()
    axs.set_xlabel('Longitude/m')  # Add an x-label to the axes.
    axs.set_ylabel('Latitude/m')  # Add a y-label to the axes.
    axs.legend();  # Add a legend.
        
def trace_with_disturbance():
    pass
    
def draw():
    fig, axs = plt.subplots(figsize=(20, 5), layout='constrained')  # a figure with a 2x2 grid of Axes
    boundary1 = Cboundary(-1.761356, -0.004106, -0.000393, -0.000012, 0, 52.81)
    boundary1.draw_polynomial(axs, boundarycolor=(1.,0.,0.,0.2))
    boundary2 = Cboundary(-1.779935, -0.004795, -0.000415, -0.000012, 0, 40.83)
    boundary2.draw_polynomial(axs, boundarycolor=(1.,0.,0.,0.3))
    boundary3 = Cboundary(-1.787721, -0.005490, -0.000436, -0.000012, 0, 30.64)
    boundary3.draw_polynomial(axs, boundarycolor=(1.,0.,0.,0.3))
    setaxsproperties(axs)
    
if __name__ == '__main__':
    np.random.seed(19680801)  # seed the random number generator.
    data = {'a': np.arange(50),
            'c': np.random.randint(0, 50, 50),
            'd': np.random.randn(50)}
    data['b'] = data['a'] + 10 * np.random.randn(50)
    data['d'] = np.abs(data['d']) * 100
    
    # x = np.linspace(0, 2, 100)  # Sample data.
    # z = np.linspace(0, 1.5, 100)  # Sample data.

    # # Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
    # fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
    # ax.plot(x, x, label='linear')  # Plot some data on the axes.
    # ax.plot(z, -z**2, label='quadratic', color=(1.,0.,0.,0.2))  # Plot more data on the axes...
    # ax.plot(x, x**3, label='cubic')  # ... and some more.
    # ax.set_xlabel('x label')  # Add an x-label to the axes.
    # ax.set_ylabel('y label')  # Add a y-label to the axes.
    # ax.set_title("Simple Plot")  # Add a title to the axes.
    # ax.legend();  # Add a legend.
    draw()
    
    print("test")