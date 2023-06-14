import main
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

def sigmoid_approximation(x, shift_position = 20, scale = 0.1):
    if  scale * (x - shift_position) <= 4 and  scale * (x - shift_position) >= 0:
        return 1-0.5*(1-0.25* scale * (x - shift_position))*(1-0.25* scale * (x - shift_position))
    elif  scale * (x - shift_position) >= -4 and  scale * (x - shift_position) < 0:
        return 0.5*(1+0.25* scale * (x - shift_position))*(1+0.25* scale * (x - shift_position))
    elif  scale * (x - shift_position) > 4:
        return 1
    else:
        return 0

def error(x):
    return main.ref_function(x, shift_position=0, scale=1) - sigmoid_approximation(x, shift_position=0, scale=1)

def draw_function():
    # draw the error of the sigmoid and its approximation segmented second order nonlinear function
    fig = plt.figure()
    ax0, ax1 = fig.subplots(1, 2, sharex=True)
    x = np.linspace(0, 10, 100)  # Sample data.
    y_error = np.array([error(_x) for _x in x])
    line0_error, = ax0.plot(x, y_error, linewidth=1);  # Plot some data on the axes.
    y_sigmoid = np.array([main.ref_function(_x, shift_position=0, scale=1) for _x in x])
    line1_error, = ax1.plot(x, y_error, linewidth=1);  # Plot some data on the axes.
    line1, = ax1.plot(x, y_sigmoid, linewidth=1);  # Plot some data on the axes.
    ax0.set_xlabel('x')  # Add an x-label to the axes.
    ax0.set_ylabel('y')  # Add a y-label to the axes.
    ax0.set_title("Sigmoid-Approximation\n error")  # Add a title to the axes.
    ax0.legend();  # Add a legend.
    ax1.set_title("Sigmoid-Approximation error\n and Sigmoid")  # Add a title to the axes.
    plt.show()

if __name__ == '__main__':
    draw_function()