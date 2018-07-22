import numpy as np
from point import point2D


class panel():
    def __init_(self):
        self.Point_0 = point2D()
        self.Point_1 = point2D()
        self.PanelIndex = -1
        self.__Omega = 0

    def calcOmega(self):
        dy = self.Point_1.y-self.Point_0.y
        dx = self.Point_1.x-self.Point_0.x
        self.__Omega = np.atan(dy/dx)

    @property
    def Omega(self):
        return self.Omega


print(__name__)
if __name__ == "__main__":
    panel1 = panel()
    print('done')
