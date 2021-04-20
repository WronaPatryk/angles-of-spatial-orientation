import EKF as EKF
import numpy as np

def basic_test():
    
    ekf = EKF.EKF()

    ekf.predict([1,1,1])
    ekf.update([1,1,1])

    print("BASIC TEST DONE")


def show_case_test(omega, a):

    ekf = EKF.EKF()

    print('PREDICT')
    ekf.predict(omega)
    #print(100*np.abs(ekf.xHatBar - predict_ans[0])/predict_ans[0])
    #print(100*np.abs(ekf.PkBar - predict_ans[1])/predict_ans[1]
    print('A matrix')
    print(ekf.A)

    print('B matrix')
    print(ekf.B)



    print('xHatBar')
    print(ekf.xHatBar)
    print('PkBar')
    print(ekf.PkBar)

    print('PREDICT')
    ekf.update(a)
    #print(100*np.abs(ekf.K - update_ans[0])/update_ans[0])
    #print(100*np.abs(ekf.xHat - update_ans[1])/update_ans[1])
    #print(100*np.abs(ekf.PkBar - update_ans[2])/update_ans[2])
    print('K')
    print(ekf.K)
    print('xHat')
    print(ekf.xHat)
    print('PkBar')
    print(ekf.PkBar)
    print(EKF.getEulerAngles(ekf.xHat[0:4]))

    print("CASE TEST DONE")



    


def run_tests():
    basic_test()
    show_case_test([0,-1,0],[-np.sin(1),0,-np.cos(1)] )


show_case_test([0,-1,0],[-np.sin(1),0,-np.cos(1)] )