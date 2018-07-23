# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 18:51:27 2018

Defining SVD of airfoils


@author: gutierrez
"""

import glob as gl
import numpy as np
from scipy import interpolate
files = gl.glob('coord_seligFmt/*')



#x=

x= linspace(0,1,500)
airfoils_list=[]
airfoil_y_coord=[]
counter=0
for airfoil_name in files:
    try:
        print(counter)
        name_airfoil = airfoil_name.split('\\')[1].split('.')[0]
        coordenadas_xy = np.loadtxt(airfoil_name,dtype=float32,skiprows=1)
        punto_remanso=argmin(abs(coordenadas_xy[:,0]))
        f_inter = interpolate.interp1d(coordenadas_xy[:punto_remanso+1,0],coordenadas_xy[:punto_remanso+1,1],kind='cubic',fill_value='extrapolate')
        y1=f_inter(x)
    #    plot(x,y1)
        f_inter = interpolate.interp1d(coordenadas_xy[punto_remanso+1:,0],coordenadas_xy[punto_remanso+1:,1],kind='cubic',fill_value='extrapolate')
        y2=f_inter(x)
    #    plot(x,y2)
        yc = array([y1, y2]).reshape(-1)
        xc = array([x, x]).reshape(-1)
        airfoils_list.append(name_airfoil)
        airfoil_y_coord.append(yc)
        counter+=1
    except Exception as e:
        print(airfoil_name)
    

#plot(xc,yc,'*')