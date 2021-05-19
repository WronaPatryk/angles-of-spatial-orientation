import tests as t
import csv
import EKF as EKF
import numpy as np

def read_case(inpath, outpath):

    g = 9.80665

    BAx = -0.21775/g
    BAy = -0.16934/g
    BAz = -9.76653/g

    #file_writer = csv.writer(open(outpath, mode='w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_reader = csv.reader(open(inpath) , delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    line_count = 0

    accelref = [BAx, BAy, BAz]

    accel = np.array(accelref).transpose()
    accelMag = (accel[0] ** 2 + accel[1] ** 2 + accel[2] ** 2) ** 0.5

    accelref = accel / accelMag

    print(accelref)



    ekf = EKF.EKF( dt = 0.02)

    bYAW = 80.97758
    bPITCH = 1.961 # Pochylanie THETA 
    bROLL = -1.371 # Przechylanie FI

    for row in file_reader:
        if line_count == 0:
            print('------------------------------')
        else:
            time = float(row[0])

            Ax = float(row[1])/g
            Ay = float(row[2])/g
            Az = float(row[3])/g

            Gx = float(row[4])
            Gy = float(row[5])
            Gz = float(row[6])

            ekf.predict([Gx * np.pi/180, Gy * np.pi/180, Gz * np.pi/180])
            ekf.update([Ax, Ay, Az])
            num = EKF.getEulerAngles(ekf.xHat[0:4])

            print('------------------------------')
            print('Gx: %.5f deg/s; Gy: %.5f deg/s; Gz: %.5f deg/s' % (Gx, Gy, Gz))
            print('Ax: %.5fg; Ay: %.5fg; Az: %.5fg' % (Ax, Ay, Az))
            print('Yaw: %.5f; Pitch: %.5f; Roll: %.5f' % num)
            print('RYaw: %.5f; RPitch: %.5f; RRoll: %.5f' % (float(row[14]) - bYAW, float(row[8]) , float(row[7]) ))

            
        line_count += 1

        if(line_count > 100): break



if __name__ == '__main__':

    read_case("data/testdata.csv","testout.csv")
