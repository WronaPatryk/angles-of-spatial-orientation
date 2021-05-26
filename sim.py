import numpy as np
from operator import add

import quaternion as quat
import EKF as EKF
import vmath as vmath
import csv

import errors

class Sensor:
    def __init__(self, 
                gnoise_mu = [0, 0, 0], 
                gnoise_std = [[0.001, 0, 0], [0, 0.001, 0], [0,0,0.001]],
                bias = 0, 
                anoise_mu = [0, 0, 0],
                anoise_std = [[0.001, 0, 0], [0, 0.001, 0], [0,0,0.001]]):
                
        self.gnoise_mu = gnoise_mu
        self.gnoise_std = gnoise_std

        self.bias = bias

        self.anoise_mu = anoise_mu
        self.anoise_std = anoise_std

    def gen_omega(self, omega):

        x, y, z = np.random.multivariate_normal(self.gnoise_mu, self.gnoise_std ).T

        #return [ omega[0] *(1+self.gnoise_std[0][0]*x), omega[1]*(1+self.gnoise_std[1][1]*y), omega[2]*(1+self.gnoise_std[2][2]*z) ]

        return [ omega[0] + self.gnoise_std[0][0]*x, omega[1] +self.gnoise_std[1][1]*y , omega[2]+self.gnoise_std[2][2]*z ]


    def gen_accel(self, a):
        x, y, z = np.random.multivariate_normal(self.anoise_mu, self.anoise_std ).T

        #return [ a[0] *(1+self.anoise_std[0][0]*x), a[1]*(1+self.anoise_std[1][1]*y), a[2]*(1+self.anoise_std[2][2]*z) ]
        return [ a[0] +self.anoise_std[0][0]*x, a[1]+self.anoise_std[1][1]*y, a[2]+self.anoise_std[2][2]*z ]


    def get_from_omega(self, omega, bquat, fbquat):

        ans = quat.quaternion(bquat, omega)

        rangs = EKF.getEulerAngles(ans[0])

        

        fomega = self.gen_omega(omega)

        fans = quat.quaternion(fbquat, fomega)

        fangs = EKF.getEulerAngles(fans[0])



        raccel = vmath.nvec(rangs)

        #faccel = self.gen_accel(raccel)

        #faccel = vmath.nvec(fangs)

        faccel = self.gen_accel(vmath.nvec(fangs))

        return (ans[0],fans[0], fomega, faccel,raccel, rangs)


sim = Sensor() 

def loop_case_test(omega, steps):
    bquat = [1,0,0,0]
    fbquat = [1,0,0,0]

    ekf = EKF.EKF()

    file_writer = csv.writer(open('data/test2.csv', mode='w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for dt in range(steps):

        bquat, fbquat, fomega, faccel, raccel, rangs  = sim.get_from_omega(omega, bquat, fbquat)


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
        file_writer.writerow(list(rangs)+list(num))



loop_case_test([0 * np.pi/180, 0 * np.pi/180, 0 * np.pi/180], 179)