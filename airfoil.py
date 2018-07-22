# -*- coding: utf-8 -*-
"""

References:
    
    
@author: gutierrez
"""
import numpy as np
import matplotlib.pyplot as mp
from stl import mesh
from  point import point2D
	

class airfoil():
    N_BernsteinPolynomial = 40
    def __init__(self):
        print('Creating new airfoil')
        self.Points_Intrados = []
        self.Points_Extrados = []
        self.DegreesRepresentation = 6
        self.Nx = 0
    def calcCSTmatrix(self):
        self.CSTmatrix=np.zeros([self.Nx,self.N_BernsteinPolynomial])
        X_extrados=self.X_extrados()
        Y_extrados=self.Y_extrados()
        for i in np.arange(self.Nx):
            for j in np.arange(self.N_BernsteinPolynomial):
                self.CSTmatrix[i,j]=airfoil.evalCST_basis_function(j,X_extrados[i])
#        print(self.CSTmatrix)
    def addPoint(self, point):
        self.Points.append(point)
        
    def addtoPointList(self, point,Points_List):
        Points_List.append(point)
    
    
    def createBernsteinFunctions(self):
        self.BernsteinFunction=[]
        #[(lambda x: (lambda y: airfoil.evalCST_basis_function(y,x)))(i) for i in np.arange(airfoil.N_BernsteinPolynomial)]
        #self.BernsteinFunction=[lambda x: airfoil.evalCST_basis_function(Nt,x) for Nt in np.arange(airfoil.N_BernsteinPolynomial)]
        self.BernsteinFunction=[(lambda x: (lambda y: airfoil.evalCST_basis_function(x,y)))(i) for i in np.arange(airfoil.N_BernsteinPolynomial)]   
        
        
    def createPointfromCoordinates(self, x,y):
        for x_i,y_i in zip(x,y):
            new_point=point2D()
            new_point.set_XYadimensional(x_i,y_i)
            self.addPoint(new_point)
    def Point_X(self):
        return(np.array([p.x_adimensional for p in self.Points]))
        
    def Point_X_of_list(self,PointsList):
        return(np.array([p.x_adimensional for p in PointsList]))
        
    def Point_Y_of_list(self,PointsList):
        return(np.array([p.y_adimensional for p in PointsList]))         
    
    def Point_Y(self):
        return(np.array([p.y_adimensional for p in self.Points]))
        
    def evalCST_basis_function(i,x_adimensional,N1=0.5,N2=1.0):
        return(airfoil.classFunction(N1=N1,N2=N2,x_adimensional=x_adimensional)*airfoil.CalcBernsteinPolynomial(i=i,n=airfoil.N_BernsteinPolynomial,x_adimensional=x_adimensional))
#        print(i)
#        return(airfoil.CalcBernsteinPolynomial(i=i,n=airfoil.N_BernsteinPolynomial,x_adimensional=x_adimensional))
#        
    
    def classFunction(N1,N2,x_adimensional):
        return(x_adimensional**N1*(1-x_adimensional)**N2)
       
    def calcBernsteinCoefficient(matrix, y):
        return(np.dot(np.linalg.pinv(matrix),y[::-1]))
    
    def adjUsingBernsteinCoefficients(self):
        y=self.Y_extrados()
        self.calcCSTmatrix()
        self.BernsteinCoeff=airfoil.calcBernsteinCoefficient(self.CSTmatrix, y)
        
        
    def CalcBernsteinPolynomial(i,n,x_adimensional):
        binomialCoeff=airfoil.CalcBinomialCoefficientK(n,i)
        return(binomialCoeff*x_adimensional**i*(1-x_adimensional)**(n-i))
        
    def CalcBinomialCoefficientK(n,i):
        fact=np.math.factorial
        return(fact(n)/(fact(i)*fact(n-i)))
        
    def extractParametersNacaName(NACALPSTT):
        optimunLift = np.int(NACALPSTT[4])
        x_Maximum_Camber = np.int(NACALPSTT[5])
        camber_Type = np.int(NACALPSTT[6])
        Maximum_Thickness = np.int(NACALPSTT[7])
        
    def X_extrados(self):
        return(np.array([p.x_adimensional for p in self.Points_Extrados]))
    def Y_extrados(self):
        return(np.array([p.y_adimensional for p in self.Points_Extrados]))
    def X_intrados(self):
        return(np.array([p.x_adimensional for p in self.Points_Intrados]))
    def Y_intrados(self):    
        return(np.array([p.y_adimensional for p in self.Points_Intrados]))
        
        
    def extractMaxThicknessNACA4Name(NACA00xx):
        return(int(NACA00xx[6:]))
    
    def createPointsfromNACAdefinition(self, x,MaxThickness):
        self.Nx = len(x)
        for x_adimensional in x:
            y_adimensional=airfoil.calc_Y_NACA_00XX(x_adimensional, MaxThickness)
            extrados_point=point2D()
            extrados_point.set_XYadimensional(x_adimensional,y_adimensional)
            intrados_point=point2D()
            intrados_point.set_XYadimensional(x_adimensional,-extrados_point.y_adimensional)
            self.addtoPointList(extrados_point,self.Points_Extrados)
            self.addtoPointList(intrados_point,self.Points_Intrados)
    
    def calc_Y_NACA_00XX(x_adimensional, MaxThickness):
        
        y_adimensional = 5*MaxThickness/100*(0.2969*np.sqrt(x_adimensional)-0.126*x_adimensional
                                             -0.3516*x_adimensional**2+0.2843*x_adimensional**3
                                             -0.1015*x_adimensional**4)
        
        return(y_adimensional)
        
        
    def loadNACA4digits_symmetrical(self,NACA00xx):
        MaxThickness = airfoil.extractMaxThicknessNACA4Name(NACA00xx)
        for point in self.Points:
            point.y_adimensional=airfoil.calc_Y_NACA_00XX(point.x_adimensional, MaxThickness)

    def plotBernsteinFunction(self):
        yb=np.zeros(len(self.Points_Intrados))
        x=self.X_extrados()
        counterf=0
        for polll in self.BernsteinFunction:
            counter=0
            for xu in x:
                yb[counter]+=polll(xu)*self.BernsteinCoeff[counterf]
                counter+=1
#            yb=np.zeros(len(self.Points_Intrados))
            counterf+=1
        mp.plot(1-x,yb)
airfoil1 = airfoil()  
      
x=np.linspace(0,1,500)
y=x**0.5*(1-x)**1
airfoil1.createPointsfromNACAdefinition(x,12)  
mp.plot(airfoil1.X_extrados(),airfoil1.Y_extrados())
mp.plot(airfoil1.X_intrados(),airfoil1.Y_intrados())
airfoil1.adjUsingBernsteinCoefficients()
airfoil1.createBernsteinFunctions()
airfoil1.plotBernsteinFunction()
