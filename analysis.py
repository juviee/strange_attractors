#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import numpy as np
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class file_printer:
    class __OnlyOne:
        def __init__(self):
            pass
    instance = None
    def __init__(self):
        if not file_printer.instance:
            file_printer.instance = file_printer.__OnlyOne()
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def write_line(self, log_line):
        with open("log.txt", 'a') as f:
            f.write(log_line + '\n')


__tau = 10

def delay_translate (src_vec, new_dim):
    '''
    Creates from [1xN] vec [Mx(N-M*__tau)] vec
    '''
    print("delay translate, tau = {}".format(__tau))
    result = list()
    for i in range (new_dim):
        tmp_vec = src_vec[i*__tau: len (src_vec) - (new_dim-i-1)*__tau]
        result.append (tmp_vec)
    return result

def distance_between_points (p1, p2):
    '''
    Calculates non-euclid distance between points
    (required by fractal_dimension calculator)'''
    #print("{} - {}".format(p1, p2))
    return abs (sum ([i - j for i in p1 for j in p2\
                    if p1.index (i) == p2.index (j)]))

def build_2d_plot (dataX, dataY, fig_name, ls = 'solid', marker = '.',
        left_xlim = None, right_xlim = None, lw = 1, ms = 0.5):
    '''builds a plot of dataX - dataY and save it to fig_name'''
    print("plotter")

    fig, m_graph = plt.subplots (1)
    m_graph.set_xlim(left_xlim, right_xlim)
    m_graph.plot (dataX, dataY, ls = ls, marker = marker, ms = ms, mec = 'black', lw = lw)
    #m_graph.set_ylim(ymin=0)
    m_graph.grid (True)
    m_graph.set_title (fig_name)

    fig.set_size_inches( 7, 7)
    fig.tight_layout ()
    fig.savefig (fig_name + ".png")


def heaviside_function (x):
    return int(x>=0)

def cr_function (src_vec, eps):
    transposed_vec = np.array (src_vec).T
    c_r = sum ( [heaviside_function(\
                    eps - distance_between_points (list(i), list(j)))\
        for i in transposed_vec for j in transposed_vec\
        if not np.array_equal (i, j)] )/((len(transposed_vec))**2)

    return c_r

def correlation_dimension (src_vec, eps):
    return np.log (cr_function (src_vec, eps))/np.log (eps)

def build_variation_of_eps (src_vec, dimension, eps_min, eps_max, iterations):
    dataY = list()
    dataX = list()
    formated_vec = delay_translate (src_vec, dimension)
    print("build_variation_of_eps")
    for eps in np.arange(eps_min, eps_max,(eps_max - eps_min)/iterations):
        c_temp = cr_function(formated_vec, eps)
        dataY.append (np.log (c_temp))
        dataX.append (np.log (eps))
        a = file_printer()
        a.write_line("x - {} || y - {}".format(eps, c_temp))
    build_2d_plot (dataX, dataY, "eps_variation")

def load_data (file_name):
    src_vec = list()
    with open (file_name) as f_in:
        while True:
            line = f_in.readline()
            if line == '':
                break
            src_vec.append (float(line))
    return src_vec

def stage_1():
    file_name = input ("data file name: ")
    src_vec = load_data (file_name)
    
    eps_min = float (input ("left boundary to search eps: "))
    eps_max = float (input ("right(exclusive) boundary to search eps: "))
    iterations = int (input ("iterations to search: "))
    build_variation_of_eps (src_vec, 2, eps_min, eps_max, iterations)

def build_variation_of_dim(src_vec, eps, min_dim, max_dim):
    dataX = list()
    dataY = list()
    for dim in range (min_dim, max_dim + 1):
        formated_vec = delay_translate (src_vec, dim)
        cr_temp = correlation_dimension (formated_vec, eps)
        dataX.append (dim)
        dataY.append (cr_temp)
        a = file_printer ()
        a.write_line ("{} - {}".format(dim, cr_temp))
    build_2d_plot (dataX, dataY, "Dimension variation")

def stage_2():
    file_name = input ("data file name: ")
    src_vec = load_data (file_name)
    eps = float (input ("eps of sphere(from stage 1): "))
    min_dim = int (input ("least dimension: "))
    max_dim = int (input ("biggest dimension: "))
    
    build_variation_of_dim(src_vec, eps, min_dim, max_dim)

    print("nope")
def stage_3():
    file_name = input ("data file name: ")
    src_vec = load_data(file_name)
    d2 = delay_translate(src_vec, 2)
    
    build_2d_plot(d2[0], d2[1], "Strange attractor", ls = 'None',
            left_xlim = -1.5, right_xlim = 0.5, ms = 1)
    build_2d_plot(d2[0], d2[1], "Strange attractor(accumulation)",  
            left_xlim = -0.75, right_xlim = 0.35, ms = 1, lw = 0.1)
    build_2d_plot(d2[0], d2[1], "Strange attractor(accumulation zoomed)", lw = 0.1,
            left_xlim = -0.0, right_xlim = 0.25, ms = 0.7)

if __name__=="__main__":
    stage = int (input ("select stage: "))
    if stage == 1:
        stage_1()
    elif stage == 2:
        stage_2()
    elif stage == 3:
        stage_3()
