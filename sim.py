import numpy as np
from operator import add

import quaternion as quat
import EKF as EKF
import vmath as vmath
import csv

import errors

def roundlst(lst,r):
    return list(map(lambda x : round(x, r), lst))

class Sensor:
    def __init__(self, 
                gnoise_mu = [0.00013, 0.00104, 0.00001], 
                gnoise_std = [[0.00426**2, 0, 0], [0, 0.00438**2, 0], [0,0,0.001**2]],
                bias = [0.01 * np.pi/180 , 0.009 * np.pi/180, 0.012 * np.pi/180], 
                anoise_mu = [0.00032, -0.00026, 0.0001],
                anoise_std = [[0.00065**2,0,0], [0, 0.00058**2,0], [0,0,0.0001*2]]):
                
        self.gnoise_mu = gnoise_mu
        self.gnoise_std = gnoise_std

        self.bias = bias

        self.anoise_mu = anoise_mu
        self.anoise_std = anoise_std

    def gen_omega(self, omega, dt):

        x, y, z = np.random.multivariate_normal(self.gnoise_mu, self.gnoise_std ).T

        #return [ omega[0] *(1+self.gnoise_std[0][0]*x), omega[1]*(1+self.gnoise_std[1][1]*y), omega[2]*(1+self.gnoise_std[2][2]*z) ]

        return [ omega[0] + omega[0] * x + self.bias[0]*dt, omega[1] + omega[1]*y + self.bias[1]*dt , omega[2]+ omega[2]*z + self.bias[1]*dt]


    def gen_accel(self, a):
        x, y, z = np.random.multivariate_normal(self.anoise_mu, self.anoise_std ).T

        #return [ a[0] *(1+self.anoise_std[0][0]*x), a[1]*(1+self.anoise_std[1][1]*y), a[2]*(1+self.anoise_std[2][2]*z) ]
        #return [ a[0] +self.anoise_std[0][0]*x, a[1]+self.anoise_std[1][1]*y, a[2]+self.anoise_std[2][2]*z ]

        #dR = np.sqrt(x**2 + y**2 + z**2)

        #return [ a[0] + x/dR, a[1] + y/dR, a[2] + z/dR ]

        #return [ a[0] + a[0] * x/dR, a[1] +a[1] * y/dR, a[2] + a[2] * z/dR ]

        #return [ a[0] + a[0] * x/dR, a[1] +a[1] * y/dR, a[2] + a[2] * z/dR ]

        return [ a[0] +x * a[0], a[1]+y * a[1], a[2] + z * a[2]]

        #return [ a[0] +x * a[0] +y * a[1]  + z * a[2] , a[1] + x * a[0] +y * a[1]  + z * a[2], a[2] + x * a[0] +y * a[1]  + z * a[2]]


    def get_from_omega(self, omega, bquat, fbquat, dt):

        r = 10

        omega = roundlst(omega, r)

        ans = quat.quaternion(bquat, omega)

        rangs = EKF.getEulerAngles(ans[0])

        

        fomega = roundlst(self.gen_omega(omega, dt), r)

        fans = quat.quaternion(fbquat, fomega)

        #fangs = EKF.getEulerAngles(fans[0])



        raccel = roundlst(vmath.nvec(rangs), r)

        #faccel = self.gen_accel(raccel)

        #faccel = vmath.nvec(fangs)

        faccel = roundlst(self.gen_accel(raccel),r)

        return (ans[0],fans[0], fomega, faccel,raccel, rangs)


sim = Sensor() 

def loop_case_test(omega, steps):
    bquat = [1,0,0,0]
    fbquat = [1,0,0,0]

    ekf = EKF.EKF()

    file_writer = csv.writer(open('data/test2.csv', mode='w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for dt in range(steps):

        bquat, fbquat, fomega, faccel, raccel, rangs  = sim.get_from_omega(omega, bquat, fbquat,dt)


        ekf.predict(fomega)

        ekf.update(faccel)

        num = EKF.getEulerAngles(ekf.xHat[0:4])

                
        cerror = errors.cape_error(rangs,num)
        omerror = errors.cape_error(omega, fomega)
        accerror = errors.cape_error(raccel, faccel)

        print('------------------------------')
        print('Yaw: %.5f; Pitch: %.5f; Roll: %.5f' % num)
        print('RYaw: %.5f; RPitch: %.5f; RRoll: %.5f' %  rangs)
        print('EYaw: %.5f; EPitch: %.5f; ERoll: %.5f' %   cerror )

        #file_writer.writerow( list(num) + list(rangs) + list(cerror))
        #file_writer.writerow(list(omega) + list(fomega) + list (raccel) + list(faccel) + list(omerror)+ list(accerror)+list(cerror))
        #file_writer.writerow( list(cerror))
        #file_writer.writerow( list(omerror)+ list(accerror)+list(cerror))
        file_writer.writerow(list(rangs)+list(num))



loop_case_test([1 * np.pi/180, 1 * np.pi/180, 1 * np.pi/180], 2900)