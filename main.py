# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 16:03:09 2016

@author: 
"""
# the suite is based on the following packages
import scipy as sp
import numpy as np
# for working with time series 
import pandas as p
# for plotting
import matplotlib.pyplot as plt
import bokeh
import datetime as dt
import math

from matplotlib.ticker import MultipleLocator, FormatStrFormatter, FuncFormatter

#seaborn
# create pandas data structure for handling the tests, speed in m/s and lactate in mmol/l

#http://www.lactate.com/questions/question_03a_what_is_threshold.html
#The transition at the higher level has to do with the capacity of the cells to utilize lactate as a fuel versus the rate at which it is being produced.
# http://www.lactate.com/Examples/m010_18.htm
# Stegmann, H., Kindermann, W. & Schnabel, A. (1981) Lactate kinetics and individual anaerobic threshold. International Journal of Sports Medicine, 2, 160‐165.

def lactate_curve_function(v, a, b, c):
    return a*v**b + c

#def pace_to_speed(min_per_k):
#    return (1/min_per_k)*1000/60

def pace_to_speed(min_per_k, sec_per_k = 0):
    return (1/(min_per_k + sec_per_k/60))*1000/60
    
def speed_to_pace(v):
    return (1/v)/60*1000

def pace_formatter(speed, pos = []): # second argument needed for plot formatter
    pace = speed_to_pace(speed)
    fractional_minutes, minutes = math.modf(pace)
    seconds = fractional_minutes * 60
    return '{}:{}'.format(int(minutes), int(seconds)) 
        
    
v = np.array([4.8, 4.3, 3.88, 3.52, 3.35])
v = pace_to_speed(v)
#v_in_mins = np.array([dt.timedelta(minutes = 4.8), dt.timedelta(minutes = 4.3), dt.timedelta(minutes = 3.88), dt.timedelta(minutes = 3.52), dt.timedelta(minutes = 3.35)], dtype = dt.timedelta) 
#[4.8, 4.3, 3.88, 3.52, 3.35]
#v.astype("timedelta64")

l = np.array([0.89, 1.28, 2.1, 4.8, 7.6])
#l = np.array([1.1, 1.48, 2.1, 3.83, 6.34])
#import step_test
from test_protocols.step_test import StepTest

test_1 = StepTest(v,l)
test_1.fit_curve()
vl4, sigma_vl4 = test_1.get_fixed_threshold(4)

#4.74
#%%
popt, pcov = sp.optimize.curve_fit(lactate_curve_function, v, l)

curve_v = np.arange(min(v),max(v),0.05 )
curve = lactate_curve_function(curve_v,popt[0], popt[1], popt[2])

f = FuncFormatter(pace_formatter)

fig, ax = plt.subplots()
ax.set_xlabel("Geschwindigkeit [m/s]")
#ax.xaxis.set_major_formatter(f)

ax2 =ax.twiny()
ax2.set_xbound(ax.get_xbound())
ax2.set_xlabel("Tempo [min/km]")

ax.plot(v,l,'o', linewidth = 2)
ax.plot(curve_v, curve, linewidth = 2)

#ax.xaxis.set_major_locator(MultipleLocator(0.5))

                                                             
plt.show()

#load test data from file, what would be an appropriate format?