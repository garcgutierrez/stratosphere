import numpy as np
import matplotlib.pyplot as mp
from stl import mesh


class point2D():
    def __init__(self):
        self.coordinate_x = 0
        self.coordinate_y = 0
        self.R = 0
        self.Omega = 0
        self.x_adimensional = 0
        self.y_adimensional = 0
        
    def set_XY(self, x, y):
        self.coordinate_x = x
        self.coordinate_y = y
        

    def set_XYadimensional(self, x_adimensional, y_adimensional):
        self.x_adimensional = x_adimensional
        self.y_adimensional = y_adimensional
        
    def adimensionarXY(self, CharacteristicLength):
        self.x_adimensional = self.x/CharacteristicLength
        self.y_adimensional = self.y/CharacteristicLength
        self.__x = self.x_adimensional
        self.__y = self.y_adimensional

    @property
    def y(self):
        return self.__y
    
    @property
    def x(self):
        return self.__x

