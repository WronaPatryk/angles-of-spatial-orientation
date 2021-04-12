import EKF as EKF

def basic_test():
    ekf = EKF.EKF()

    ekf.predict([1,1,1])
    ekf.update([1,1,1])

    print("BASIC TEST DONE")


def run_tests():
    basic_test()