# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 17:40:17 2018

References:
    Falck- Trajectory Optimization of Electric Aircraft

@author: gutierrez
"""

import numpy as np


class propeller():
    Ct = 0
    N = 0 
    diam = 0
    def __init__(self):
        print('Creating new propeller')
        
        
    def calculateThrust(self,rho):
        self.Ft = 2*self.Ct*rho*(self.N/60)*self.diam^4

    def calculateCt(self):
        self.Ct = self.Cp*self.etap/self.Jp
        
    def calculateCp(self, rho):
        self.Co = self.Pshaft/(rho*(self.N/60)^3*self.diam^5)
        
    def  calculateEthap(self, functionRend, ShaftTorque,Jp):
        self.etap = functionRend(ShaftTorque,Jp)
    
    def calculateJprop(self): # advance ratio
        self.Jprop = 60*self.va/self.N/self.diam
        
    def calculateShaftTorque(self): # shaft torque
        self.ShaftTorque= 60*self.Pshaft/(2*np.pi*self.N)
        
        