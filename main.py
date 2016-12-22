# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 16:03:09 2016

@author: Ägge
"""
# the suite is based on the following packages
import scypy as sp
import numpy as np
# for working with time series 
import pandas as p
# for plotting
import matplotlib as ml
import bokeh
#seaborn
# create pandas data structure for handling the tests, speed in m/s and lactate in mmol/l


# routines for non-linear regression (functions of type speed = a*lactate^b + c)
# report the accuracy of the fit
# lactate_curve(data_structure)

# routines for determining lactate threshold
# fixed_threshold(data_structure, lactate)
# model_threshold(data_structure, model)

# object oriented? object "step_test", "get_threshold", "get_min", "get_max"