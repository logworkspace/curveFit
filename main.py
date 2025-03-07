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


class CEgoMotion:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Cboundary:
    def __init__(self, c0, c1, c2, c3, startX, endX):
        self.c0 = c0
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.startX = startX
        self.endX = endX
        
    def calculateY_list(self, x):
        y_list = np.array([self.c0  + self.c1 * _x + 1.0/2.0*self.c2 * math.pow(_x, 2) + 1.0/6.0*self.c3 * math.pow(_x, 3) for _x in x])
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
    
    axs.axis([0, 70, -10, 10])
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
    fig, axs = plt.subplots(figsize=(70, 10), layout='constrained')  # a figure with a 2x2 grid of Axes
    bnds = [Cboundary(-1.761356, -0.004106, -0.000393, -0.000012, 0, 52.81),
            Cboundary(-2.779935, -0.000795, -0.000415, -0.000012, 0, 40.83),
            Cboundary(-3.787721, -0.005490, -0.000436, -0.000012, 0, 30.64),
            Cboundary(-4.779935, -0.009795, -0.000415, -0.000012, 0, 40.83),
            Cboundary(-5.787721, -0.006490, -0.000436, -0.000012, 0, 30.64)
            ]

    set_axs_properties(axs)
    ani = animation.FuncAnimation(
    fig, partial(draw_boundary, boundaries=bnds,count=store_num, axs=axs), interval=1000, blit=True, save_count=50)
    plt.show()

def transform(boundary_orig):
    return boundary_orig

def ref_function(x, shift_position = 20, scale = 0.1):
    y = 1 / (1 +  math.exp(-1 * scale * (x - shift_position)))
    return y

def linspace(start, end, space):
    return np.linspace(start, end, int((end - start) / space + 1))

def merge_polynomial(former_boundary, later_boundary, ref_function):

    common_start = max(former_boundary.startX, later_boundary.startX)
    common_end = min(former_boundary.endX, later_boundary.endX)
    if common_end < common_start + 3:
        return later_boundary, ()
    min_start = min(former_boundary.startX, later_boundary.startX)

    end = later_boundary.endX
    space = 2.5
    if common_start - min_start > 3*space:
        prefix_x = linspace(min_start, common_start - space, space)
    else:
        prefix_x = np.array([])
    common_x = linspace(common_start, common_end, space)
    if end - common_end > 3*space:
        suffix_x = linspace(common_end + space, end, space)
    else:
        suffix_x = np.array([])
    # x_list = np.concatenate((prefix_x, common_x, suffix_x), axis=0)

    common_x_count = len(common_x)
    former_common_latitude = former_boundary.calculateY_list(common_x)
    later_common_latitude = later_boundary.calculateY_list(common_x)
    coeff_common = [ref_function(x, end*0.5, (common_end-common_start)*0.5*0.0006) for x in common_x]
    merge_common_latitude = np.array([(1-coeff_common[index])*former_common_latitude[index] + coeff_common[index]*later_common_latitude[index] for index in list(range(common_x_count))])
    
    prefix_x_count = len(prefix_x)
    former_prefix_latitude = former_boundary.calculateY_list(prefix_x)
    later_prefix_latitude = later_boundary.calculateY_list(prefix_x)
    if former_common_latitude.size > 0:
        if later_boundary.startX > former_boundary.startX:
            common_start_shift = coeff_common[0]*(later_common_latitude[0] - former_common_latitude[0])
            merge_prefix_latitude = [former_prefix_latitude[index]+common_start_shift for index in list(range(prefix_x_count))]
            merge_prefix_latitude = np.array(merge_prefix_latitude)
        else:
            common_start_shift = (1-coeff_common[0])*(former_common_latitude[0] - later_common_latitude[0])
            merge_prefix_latitude = [later_prefix_latitude[index]+common_start_shift for index in list(range(prefix_x_count))]
            merge_prefix_latitude = np.array(merge_prefix_latitude)
    else:
        merge_prefix_latitude = np.array([])

    merge_suffix_latitude = later_boundary.calculateY_list(suffix_x)
    merge_latitude = np.concatenate((merge_prefix_latitude,merge_common_latitude))
    merge_latitude = np.concatenate((merge_latitude, merge_suffix_latitude))
    merge_longitude = np.concatenate((np.concatenate((prefix_x, common_x)), suffix_x))
    polynomial_function = np.polyfit(merge_longitude, merge_latitude, 3)
    # polynomial3 = np.poly1d(polynomial_function)

    if prefix_x.size > 0:
        start_x = prefix_x[0]
    elif common_x.size > 0:
        start_x = common_x[0]
    elif suffix_x.size > 0:
        start_x = suffix_x[0]

    if suffix_x.size > 0:
        end_x = suffix_x[-1]
    elif common_x.size > 0:
        end_x = common_x[-1]
    elif prefix_x.size > 0:
        end_x = prefix_x[-1]

    boundary_merged = Cboundary(polynomial_function[3], polynomial_function[2],2*polynomial_function[1],6*polynomial_function[0], start_x, end_x)
    print('Fitting polynomial function coefficient(x^3, x^2, x^1, x^0): ', polynomial_function)
    return boundary_merged, (merge_longitude, merge_latitude)

class callback_manager:
    def __init__(self, fig, ax, data_list, history_cache_number=2):
        self.fig = fig
        self.ax = ax
        self.data_list = data_list
        self.index_position = -1
        self.history_cache_number = history_cache_number
        self.history_cache = []
        self.merged_cache = []
        self.merged_points_list = []
        self.merged_list = []
        data_count = len(self.data_list)
        for index in list(range(data_count)):
            data = self.data_list[index]
            boundary = data[1]
            boundary = transform(boundary)
            if index == 0:
                self.merged_list.append((boundary,()))
                continue
            boundary_former = self.merged_list[-1][0]
            boundary_former = transform(boundary_former)
            merged = merge_polynomial(boundary_former, boundary, ref_function)
            self.merged_list.append(merged)

    def clear_all_history(self):
        for history_line in self.history_cache:
            history_line.remove()
        self.history_cache = []

        for history_line in self.merged_cache:
            history_line.remove()
        self.merged_cache = []

        for history_points in self.merged_points_list:
            history_points.remove()
        self.merged_points_list = []

    def on_press(self, event):
        print('press', event.key)
        list_len = len(self.data_list)
        if not list_len or (event.key == 'left' and event.key == 'right'):
            return
        if event.key == 'left':
            self.index_position = self.index_position - 1
        elif event.key == 'right':
            self.index_position = self.index_position + 1
        elif event.key == 'r':
            plt.cla()
            print('clear fig!')
            # for item in self.exist_history:
            #     item.remove()
            #     print('Removed!')
            set_axs_properties(self.ax)
            return
        self.index_position = min(list_len - 1, max(0, self.index_position))
        print(self.index_position, 'index')

        # if self.exist_history is not None:
        #     self.exist_history.remove()
        self.clear_all_history()

        for index in list(range(self.history_cache_number)):
            index_cropped = min(list_len - 1, max(0, self.index_position - index))
            data = self.data_list[index_cropped]
            boundary = data[1]
            boundary = transform(boundary)
            line_drawed = boundary.draw_polynomial(self.ax, boundarycolor=(1.,0.,0.,1.0 / (2*index+1)), linewidth = max(1, 2-index))
            self.history_cache.append(line_drawed)
            merged_data = self.merged_list[index_cropped]
            boundary_merged = merged_data[0]
            line_drawed_merged = boundary_merged.draw_polynomial(self.ax, boundarycolor=(0.,0.,1.,1.0 / (2*index+1)), linewidth = max(1, 2-index))
            self.merged_cache.append(line_drawed_merged)
            merged_points = merged_data[1]
            if merged_points != ():
                points_drawing = self.ax.scatter(merged_points[0], merged_points[1], s=30 - 9*index)
                self.merged_points_list.append(points_drawing)



        # for index in list(range(self.history_cache_number)):
        #     index_cropped = min(list_len - 1, max(0, self.index_position - index))
        #     data = self.data_list[index_cropped]
        #     boundary = data[1]
        #     boundary = transform(boundary)
        #     index_former_cropped = min(list_len - 1, max(0, self.index_position - index - 1))
        #     if index_former_cropped < index_cropped:
        #         boundary_former = self.data_list[index_former_cropped][1]
        #         index_former_former_cropped = min(list_len - 1, max(0, self.index_position - index - 2))
        #         if index_former_former_cropped < index_former_cropped:
        #             boundary_former_former = self.data_list[index_former_former_cropped][1]
        #             boundary_former_former = transform(boundary_former_former)
        #             boundary_former_merged, merge_points_former = merge_polynomial(boundary_former_former, boundary, ref_function)
        #             points_drawing, = self.ax.plot(merge_points_former[0], merge_points_former[1], 'go')
        #             self.merged_points_list.append(points_drawing)
        #             boundary_former = boundary_former_merged
        #         else:
        #             boundary_former = transform(boundary_former)
        #         boundary_merged, merge_points = merge_polynomial(boundary_former, boundary, ref_function)
        #         line_drawed_merged = boundary_merged.draw_polynomial(self.ax, boundarycolor=(0.,0.,1.,1.0 / (2*index+1)))
        #         self.merged_cache.append(line_drawed_merged)

            
        current_index = min(list_len - 1, max(0, self.index_position))
        image_number = self.data_list[current_index][0]
        self.ax.set_title(image_number)
        event.canvas.draw()

        # if event.key == 'x':
        #     visible = xl.get_visible()
        #     xl.set_visible(not visible)
        #     fig.canvas.draw()

def function_keypress():
    fig, ax = plt.subplots(figsize=(20, 5), layout='constrained')
    data_list = parse_csv('test.csv')
    
    set_axs_properties(ax)
    callback_obj = callback_manager(fig, ax, data_list) 

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
    data_list = []
    with open(file_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            row_parsed = row[0]
            row_split = row_parsed.split(',')
            row_split_converted = [float(item) for item in row_split]
            data_list.append([int(row_split_converted[0]), Cboundary(row_split_converted[1],row_split_converted[2], row_split_converted[3],row_split_converted[4],row_split_converted[5],row_split_converted[6]),
                              CEgoMotion(row_split_converted[7], row_split_converted[8])])
            # print(row)

    return data_list

def random_sample():
    np.random.seed(19680801)  # seed the random number generator.
    data = {'a': np.arange(50),
            'c': np.random.randint(0, 50, 50),
            'd': np.random.randn(50)}
    data['b'] = data['a'] + 10 * np.random.randn(50)
    data['d'] = np.abs(data['d']) * 100

def display_sample():
    ##### test0
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
    ##### test0
    
    # draws() # test1
    # anim_history(3) # test2
    function_keypress() # test3
    
if __name__ == '__main__':
    display_sample()
    # data_list = parse_csv('test.csv')
    # draw_comparing_polynomial_adapting()
    print("#test")