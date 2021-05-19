import numpy as np
from operator import add

class Sensor:
    def __init__(self, gnoise, bias, anoise ):
        self.gnoise = gnoise
        self.bias = bias
        self.anoise = anoise

    def gen_omega(self, omega):
        return list(map(add, omega , [i * np.random.normal(0, 1) for i in self.gnoise]))

    def gen_accel(self, a):
        return list(map(add, a , [i * np.random.normal(0, 1) for i in self.anoise]))
        

