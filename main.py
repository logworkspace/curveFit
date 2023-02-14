# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a curve fitting script file.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import math
from functools import partial
from matplotlib.backend_bases import MouseButton
import csv

class Cboundary:
    def __init__(self, c0, c1, c2, c3, startX, endX):
        self.c0 = c0
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.startX = startX
        self.endX = endX
        
    def calculateY_list(self, x):
        y_list = [self.c0  + self.c1 * _x + 1.0/2.0*self.c2 * math.pow(_x, 2) + 1.0/6.0*self.c3 * math.pow(_x, 3) for _x in x]
        return y_list
    
    def draw_polynomial(self, ax, boundarycolor='orange', linewidth=1):
        x = np.linspace(self.startX, self.endX, 100)  # Sample data.
        y = self.calculateY_list(x)
        line, = ax.plot(x, y, color=boundarycolor, linewidth=linewidth);  # Plot some data on the axes.
        # ax.annotate(
        #     'straight',
        #     xy=(x[5], y[5]), xycoords='data',
        #     xytext=(-50, 30), textcoords='offset points',
        #     arrowprops=dict(arrowstyle="->"))

        return line
    
    def set_coeff(self, c0, c1, c2, c3, startX, endX):
        self.c0 = c0
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.startX = startX
        self.endX = endX
        
    def get_discrete_points(self, gap):
        #point_x = 
        return
    
def set_axs_properties(axs):

    # Move the left and bottom spines to x = 0 and y = 0, respectively.
    axs.spines[["left", "bottom"]].set_position(("data", 0))
    # Hide the top and right spines.
    axs.spines[["top", "right"]].set_visible(False)
    
    # Draw arrows (as black triangles: ">k"/"^k") at the end of the axes.  In each
    # case, one of the coordinates (0) is a data coordinate (i.e., y = 0 or x = 0,
    # respectively) and the other one (1) is an axes coordinate (i.e., at the very
    # right/top of the axes).  Also, disable clipping (clip_on=False) as the marker
    # actually spills out of the axes.
    axs.plot(1, 0, ">k", transform=axs.get_yaxis_transform(), clip_on=False)
    axs.plot(0, 1, "^k", transform=axs.get_xaxis_transform(), clip_on=False)
    
    axs.axis([-5, 70, -10, 10])
    axs.set_aspect('equal', adjustable='datalim')
    axs.grid(ls='--')
    axs.set_xlabel('Longitude/m')  # Add an x-label to the axes.
    axs.set_ylabel('Latitude/m')  # Add a y-label to the axes.
    axs.legend();  # Add a legend.
        
def trace_with_disturbance():
    pass
    
def draws():
    fig, axs = plt.subplots(figsize=(20, 5), layout='constrained')  # a figure with a 2x2 grid of Axes
    boundary1 = Cboundary(-1.761356, -0.004106, -0.000393, -0.000012, 0, 52.81)
    boundary1.draw_polynomial(axs, boundarycolor=(1.,0.,0.,0.2))
    boundary2 = Cboundary(-1.779935, -0.004795, -0.000415, -0.000012, 0, 40.83)
    boundary2.draw_polynomial(axs, boundarycolor=(1.,0.,0.,0.3))
    boundary3 = Cboundary(-1.787721, -0.005490, -0.000436, -0.000012, 0, 30.64)
    boundary3.draw_polynomial(axs, boundarycolor=(1.,0.,0.,0.3))

    set_axs_properties(axs)
    plt.show()

    
def draw_boundary(frame, boundaries, count, axs):
    print(frame, "framenumber")
    lines = []
    for i in list(range(count)):
        index = max(0, min(len(boundaries) - 1, frame - i))
        line = boundaries[index].draw_polynomial(axs, boundarycolor=(1.,0.,0.,1.0/(1 + i*3)))
        lines.append(line)
        if index ==  0:
            break
        
    return tuple(lines)

def anim_history(store_num):
    fig, axs = plt.subplots(figsize=(20, 5), layout='constrained')  # a figure with a 2x2 grid of Axes
    bnds = [Cboundary(-1.761356, -0.004106, -0.000393, -0.000012, 0, 52.81),
            Cboundary(-2.779935, -0.000795, -0.000415, -0.000012, 0, 40.83),
            Cboundary(-3.787721, -0.005490, -0.000436, -0.000012, 0, 30.64),
            Cboundary(-4.779935, -0.009795, -0.000415, -0.000012, 0, 40.83),
            Cboundary(-5.787721, -0.006490, -0.000436, -0.000012, 0, 30.64),
            ]

    set_axs_properties(axs)
    ani = animation.FuncAnimation(
    fig, partial(draw_boundary, boundaries=bnds,count=store_num, axs=axs), interval=1000, blit=True, save_count=50)
    plt.show()

class callback_manager:
    def __init__(self, fig, ax, boundary_list, base_image_count):
        self.fig = fig
        self.ax = ax
        self.boundary_list = boundary_list
        self.index = 0
        self.clear = False
        self.base_image_count = base_image_count
        
    def on_press(self, event):
        print('press', event.key)
        list_len = len(self.boundary_list)
        if not list_len or (event.key == 'left' and event.key == 'right'):
            return
        if event.key == 'left':
            self.index = self.index - 1
        elif event.key == 'right':
            self.index = self.index + 1
        elif event.key == 'r':
            plt.cla()
            print('clear fig!')
            self.clear = True
            return
        self.index = min(list_len - 1, max(0, self.index))
        print(self.index, 'index')
        if self.clear:
            set_axs_properties(self.ax)
            self.clear = False
        self.boundary_list[self.index].draw_polynomial(self.ax, boundarycolor=(1.,0.,0.,1.0))
        self.ax.set_title(self.index * 3 + self.base_image_count)
        event.canvas.draw()

        # if event.key == 'x':
        #     visible = xl.get_visible()
        #     xl.set_visible(not visible)
        #     fig.canvas.draw()
        
def function_keypress():
    fig, ax = plt.subplots(figsize=(20, 5), layout='constrained')
    bnds = [Cboundary(-1.761356, -0.004106, -0.000393, -0.000012, 0, 52.81),
            Cboundary(-2.779935, -0.000795, -0.000415, -0.000012, 0, 40.83),
            Cboundary(-3.787721, -0.005490, -0.000436, -0.000012, 0, 30.64)
            ]
    
    set_axs_properties(ax)
    callback_obj = callback_manager(fig, ax, bnds, 32) 

    fig.canvas.mpl_connect('key_press_event', callback_obj.on_press)
    # np.random.seed(19680801)
    # ax.plot(np.random.rand(12), np.random.rand(12), 'go')
    # xl = ax.set_xlabel('easy come, easy go')
    
    plt.show()

def draw_polynomial_adapting(x_list, y_list, ax, boundarycolor='orange', linewidth=1):
    polynomial_function = np.polyfit(x_list, y_list, 3)
    print('Fitting polynomial function coefficient(x^3, x^2, x^1, x^0): ', polynomial_function)
    polynomial3 = np.poly1d(polynomial_function)
    y_list_polyfit = [polynomial3(x_value) for x_value in x_list]
    ax.plot(x_list, y_list_polyfit, 'go')
    y_list_polyfit_shifted = [y + 0.05 for y in y_list_polyfit]
    line, = ax.plot(x_list, y_list_polyfit_shifted, color=boundarycolor, linewidth=linewidth);  # Plot some data on the axes.
    return line      
  
def draw_comparing_polynomial_adapting():
    # draw two cases for comparsion
    fig, axs = plt.subplots(figsize=(20, 5), layout='constrained')  # a figure with a 2x2 grid of Axes
    boundary1 = Cboundary(-1.761356, -0.002312, -0.000036, 0.000280, 0, 35.81)
    boundary1.draw_polynomial(axs, boundarycolor=(1.,0.,0.,0.2))
    x = np.linspace(boundary1.startX, boundary1.endX, 10)  # Sample data.
    y = boundary1.calculateY_list(x)
    draw_polynomial_adapting(x, y, axs)

    set_axs_properties(axs)
    plt.show()
    
def parse_csv(file_path):
    # TODO
    with open(file_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))
    return
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
    #draws()
    # anim_history(3)
    # function_keypress()
    draw_comparing_polynomial_adapting()
    print("#test")