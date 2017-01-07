# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 18:28:51 2016

@author: Ägge
"""
import scipy as sp
import numpy as np
import math 

 

class StepTest:
    
    # different functions:
        # a*s^b + b
        # a + b*s + c*s^2 + d*s^3
        # piecewise linear function
    
    def __init__(self, speed = [], lactate = [], date = []):
        self.speed = speed
        self.lactate = lactate
        self.date = date
        self.lactate_unscertainty = []
        
        self.curve_parameters = []
        self.unscertainties = []

        #from datetime import date        
        #datetime.date(2007, 12, 5)
     
    
    def lactate_curve_function(self, speed, a, b, c): # speed is the independent variable
        return a*speed**b + c     
        
    def fit_curve(self):    
        self.curve_parameters, self.unscertainties = sp.optimize.curve_fit(self.lactate_curve_function, self.speed, self.lactate)    
    
    def get_curve_point(self, speed):
        return self.lactate_curve_function(speed, self.curve_parameters[0], self.curve_parameters[1], self.curve_parameters[2])    
    
    def get_derivative(self, speed):
        return self.curve_parameters[0]*self.curve_parameters[1]*speed**(self.curve_parameters[1]-1)
        
    def get_fixed_threshold(self, threshold):      
        
        # depending on the test protocol and the type of the regression function, there might be more than one solutions!
        speed = ((threshold - self.curve_parameters[2]) / self.curve_parameters[0]) ** (1/self.curve_parameters[1])
        
        a = self.curve_parameters[0]
        b = self.curve_parameters[1]
        c = self.curve_parameters[2]
        y = threshold
        
        dda = -(((y-c)/a)**(1/b)) / (a*b)
        ddb = -((((y-c)/a)**(1/b)) * math.log((y-c)/a)) / b**2
        ddc =  (((y-c)/a)**(1/b)) / (b * (c-y))
        
        A = np.matrix([dda, ddb, ddc])
        speed_unscertainty = A * self.unscertainties * np.transpose(A) 
        
        return speed, math.sqrt(speed_unscertainty)
        
    def get_model_threshold(self):
        # Stegmann, Kindermann: setzt spezielles Protokoll voraus (Messung alle 3 min nach Belastung)
        # finde Punkt der Kurve in der Belastungsphase, an dem die Laktatkonzentration der Konzentration nach der letzten gelaufenen Stufe is
        # finde den Punkt der Kurve, in dem die Tangente den zuvor gefundenen Punkt schneidet
        # benötigt Polynom- oder Spline-Interpolation
        
        # 1. compute regression with respect to time - instead of speed!?  (3rd order polynomial or spline)
        # 2. find find time after end of the test at which the lactate level is the same as at the last test stage ("Point B").
        # 3. system of equations that help us to find "point A", which is the Kindermann IAS
        #       f(B) = B, y = ax+ b, a = y
        
        return 0