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
import yaml

from test_protocols.step_test import StepTest

from matplotlib.ticker import MultipleLocator, FixedLocator, FormatStrFormatter, FuncFormatter

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
    return '{mm}:{ss:02d}'.format(mm = int(minutes), ss = int(round(seconds,1))) 
        
#%%    
v = np.array([4.8, 4.3, 3.88, 3.52, 3.35])
v = pace_to_speed(v)
#v_in_mins = np.array([dt.timedelta(minutes = 4.8), dt.timedelta(minutes = 4.3), dt.timedelta(minutes = 3.88), dt.timedelta(minutes = 3.52), dt.timedelta(minutes = 3.35)], dtype = dt.timedelta) 
#[4.8, 4.3, 3.88, 3.52, 3.35]
#v.astype("timedelta64")

#sdfdhakjgalwgfwelhfgewALFHJG

l = np.array([0.89, 1.28, 2.1, 4.8, 7.6])
#l = np.array([1.1, 1.48, 2.1, 3.83, 6.34])
#import step_test
from test_protocols.step_test import StepTest

test_1 = StepTest(v,l)
test_1.fit_curve()

sigma_vl3 = test_1.get_fixed_threshold(3)
vl4, vl2, sigma_vl2 = test_1.get_fixed_threshold(2)
vl3,sigma_vl4 = test_1.get_fixed_threshold(4)

plt.figure()
plt.errorbar(1,vl4, xerr=0, yerr=sigma_vl4, fmt='.', color='black')
plt.errorbar(1,vl3, xerr=0, yerr=sigma_vl3, fmt='.', color='black')
plt.errorbar(1,vl2, xerr=0, yerr=sigma_vl2, fmt='.', color='black')
plt.show()
#fig.autofmt_xdate()

#4.74
#%%
popt, pcov = sp.optimize.curve_fit(lactate_curve_function, v, l)

curve_v = np.arange(min(v),max(v),0.05)
curve = lactate_curve_function(curve_v,popt[0], popt[1], popt[2])

f = FuncFormatter(pace_formatter)

fig, ax = plt.subplots()
ax.set_xlabel("Geschwindigkeit [m/s]")
ax.set_ylabel("Laktat [mmol/l]")

ax.plot(v,l,'o', linewidth = 2)
ax.plot(curve_v, curve, linewidth = 2)

ax.xaxis.set_major_locator(MultipleLocator(0.2))
ax.xaxis.set_minor_locator(MultipleLocator(0.1))

ax2 = ax.twiny()
ax2.set_xbound(ax.get_xbound()[0],ax.get_xbound()[1])

pace_locators = np.arange(180,300,10)

ax2.xaxis.set_major_locator(FixedLocator(pace_to_speed(0,pace_locators)))
ax2.set_xlabel("Tempo [min/km]")
ax2.xaxis.set_major_formatter(f)
plt.xticks(rotation=45)
                                                             
plt.show()
#%%

# load test data from yaml file. This works very easily and is beatifull :-)
test_file = open('C:/Python/lactate-analysis/data/tests.yaml')
test_data = yaml.load(test_file)
# the test data are now accessible as dictionaries

tests = []

for t in test_data:
    
    speed = pace_to_speed(np.array(t['pace']))
    lactate = np.array(t['lactate'])
    
    tests.append(StepTest(speed,lactate,t['date']))
   
for st in tests: # the constructor is not yet perfect, so call:
    st.fit_curve()
#%%   
    
#curve_v = np.arange(min(v),max(v),0.05)
#curve = lactate_curve_function(curve_v,popt[0], popt[1], popt[2])

f = FuncFormatter(pace_formatter)

fig, ax = plt.subplots()
ax.set_xlabel("Geschwindigkeit [m/s]")
ax.set_ylabel("Laktat [mmol/l]")

for st in tests:   
    
    ax.plot(st.speed,st.lactate,'-o', linewidth = 2, label = st.date)
    #ax.plot(curve_v, curve, linewidth = 2)
    #popt, pcov = sp.optimize.curve_fit(lactate_curve_function, v, l)
    #curve_v = np.arange(min(v),max(v),0.05)
    #curve = lactate_curve_function(curve_v,popt[0], popt[1], popt[2])
    
ax.xaxis.set_major_locator(MultipleLocator(0.2))
ax.xaxis.set_minor_locator(MultipleLocator(0.1))

plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.) 
   
ax2 = ax.twiny()
ax2.set_xbound(ax.get_xbound()[0],ax.get_xbound()[1])

pace_locators = np.arange(180,300,10)

ax2.xaxis.set_major_locator(FixedLocator(pace_to_speed(0,pace_locators)))
ax2.set_xlabel("Tempo [min/km]")
ax2.xaxis.set_major_formatter(f)
ax2.grid(axis='x')
ax.grid(axis='y')
plt.xticks(rotation=45)
                                                                 
plt.show()

#%%

import matplotlib.dates as mdates

vl2_list = []
vl3_list = []
vl4_list = []

sigma_vl2_list = []
sigma_vl3_list = []
sigma_vl4_list = []

date_list = []

for st in tests:   

    date_list.append(st.date)
    
    vl2, sigma_vl2 = st.get_fixed_threshold(2)
    vl3, sigma_vl3 = st.get_fixed_threshold(3)   
    vl4, sigma_vl4 = st.get_fixed_threshold(4)

    vl2_list.append(vl2)
    vl3_list.append(vl3)
    vl4_list.append(vl4)
    
    sigma_vl2_list.append(sigma_vl2)
    sigma_vl3_list.append(sigma_vl3)
    sigma_vl4_list.append(sigma_vl4)

date_list = mdates.date2num(date_list)    
    
fig, ax = plt.subplots()
ax.set_ylabel("Geschwindigkeit [m/s]")
ax.xaxis_date()

plt.errorbar(date_list, vl2_list, xerr=0, yerr=sigma_vl2_list, fmt='-o', color='green', label='vl2 (AT)') 
plt.errorbar(date_list, vl3_list, xerr=0, yerr=sigma_vl3_list, fmt='-o', color='orange', label='vl3')
plt.errorbar(date_list, vl4_list, xerr=0, yerr=sigma_vl4_list, fmt='-o', color='red', label='vl4 (AnT)')  

ax.xaxis.set_major_locator(FixedLocator(date_list))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

plt.legend(bbox_to_anchor=(1.15, 1), loc=2, borderaxespad=0.)
plt.title('Schwellenentwicklung')

pace_locators = np.arange(180,300,5)
ay2 = ax.twinx()
ay2.set_ybound(ax.get_ybound()[0],ax.get_ybound()[1])
ay2.yaxis.set_major_locator(FixedLocator(pace_to_speed(0,pace_locators)))
ay2.set_ylabel("Tempo [min/km]")
ay2.yaxis.set_major_formatter(f)  

ay2.grid(axis='y')
ax.grid(axis='x')  

#ay2.grid(True)
    
plt.show()
