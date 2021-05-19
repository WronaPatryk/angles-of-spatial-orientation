import EKF as EKF
import numpy as np
from operator import add

def basic_test():
    
    ekf = EKF.EKF()

    ekf.predict([1,1,1])
    ekf.update([1,1,1])

    print("BASIC TEST DONE")


def basic_case_test(omega, a):

    ekf = EKF.EKF()
    ekf.predict(omega)
    ekf.update(a)

    print('Yaw: %.5f; Pitch: %.5f; Roll: %.5f' % EKF.getEulerAngles(ekf.xHat[0:4]))

    print("CASE TEST DONE\n")

def loop_case_test(omega, steps):

    ekf = EKF.EKF()

    for dt in range(steps):
        ekf.predict(omega)
        ekf.update([-np.sin(-omega[1]*(dt+1)),0,-np.cos(-omega[1]*(dt+1))])
        print('Yaw: %.5f; Pitch: %.5f; Roll: %.5f' % EKF.getEulerAngles(ekf.xHat[0:4]))

    print("CASE TEST DONE\n")


    
def loop_case_with_noise(omega,steps, noise):
    ekf = EKF.EKF()

    for dt in range(steps):
        nomega = list(map(add, omega , [i * np.random.normal(0, 1) for i in noise]))
        ekf.predict(nomega)
        ekf.update([-np.sin(-omega[1]*(dt+1)), 0, -np.cos(-omega[1]*(dt+1))])
        print('Yaw: %.5f; Pitch: %.5f; Roll: %.5f' % EKF.getEulerAngles(ekf.xHat[0:4]))

    print("CASE TEST DONE\n")

def run_tests():
    basic_test()
    basic_case_test([0,-1,0],[-np.sin(1),0,-np.cos(1)] )


#basic_case_test([0,-1,0],[-np.sin(1),0,-np.cos(1)] )
#basic_case_test([0,0,0],[0,0,-1] )

#loop_case_test([0, 10*np.pi/180, 0], 5)
#loop_case_test([0, 10*np.pi/180, 0], 9)
#loop_case_with_noise([0, 0, 0], 1000, [0.001, 0.001, 0.001])

