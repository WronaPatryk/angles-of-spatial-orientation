import numpy as np

def cape_error(real,sim):
    def apx(x,y):
        if(x == 0): return 0
        return (y-x)/x
    return (apx(real[0], sim[0]),apx(real[1], sim[1]), apx(real[2], sim[2]) )

def approx_error(real, sim):
    def apx(x,y):
        return abs((y-x)/x)
    return (apx(real[0], sim[0]),apx(real[1], sim[1]), apx(real[2], sim[2]) )

def relative_error(real,sim):
    def apx(x,y):
        return y-x
    return (apx(real[0], sim[0]),apx(real[1], sim[1]), apx(real[2], sim[2]) )


def tan_error(real, sim):
    def apx(x,y):
        return np.arctan(y-x)/(np.pi/2)
    return (apx(real[0], sim[0]),apx(real[1], sim[1]), apx(real[2], sim[2]) )

def cape_tan_error(real, sim):
    def apx(x,y):
        return np.arctan(y-x/x)/(np.pi/2)
    return (apx(real[0], sim[0]),apx(real[1], sim[1]), apx(real[2], sim[2]) )
