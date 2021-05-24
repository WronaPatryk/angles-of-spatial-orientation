import tests as t
import csv
import EKF as EKF
import numpy as np


def approx_error(real, sim):
    def apx(x,y):
        return abs((x-y)/x)
    return (apx(real[0], sim[0]),apx(real[1], sim[1]), apx(real[2], sim[2]) )


def read_case(inpath, outpath, ekf):

    start_time = 0

    g = 9.80665

    file_writer = csv.writer(open(outpath, mode='w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_reader = csv.reader(open(inpath) , delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    line_count = 0

    for row in file_reader:
        if line_count == 0:
            print('------------------------------')
            old_time = 0
        else:

            time = float(row[0])

            if(time >= start_time):

                dt = time - old_time

                ekf.set_step(dt)

                old_time = time

                Ax = float(row[1])/g
                Ay = float(row[2])/g
                Az = float(row[3])/g

                Q = float(row[4])
                P = float(row[5])
                R = float(row[6])

                rangles = (float(row[14]), float(row[8]) , float(row[7]))

                ekf.predict([P * np.pi/180, Q * np.pi/180, R * np.pi/180])
                ekf.update([Ax, Ay, Az])
                num = EKF.getEulerAngles(ekf.xHat[0:4])

                aerror = approx_error(rangles, num)

                print('------------------------------')
                print('Time: %.5f sek; dt: %.5f sek' %(time, dt))
                print('Gx: %.5f deg/s; Gy: %.5f deg/s; Gz: %.5f deg/s' % (P, Q, R))
                print('Ax: %.5fg; Ay: %.5fg; Az: %.5fg' % (Ax, Ay, Az))
                print('Yaw: %.5f; Pitch: %.5f; Roll: %.5f' % num)
                print('RYaw: %.5f; RPitch: %.5f; RRoll: %.5f' %  rangles)
                print('EYaw: %.5f; EPitch: %.5f; ERoll: %.5f' %   aerror )

                file_writer.writerow([time]+ list(num) + list(rangles) + list(aerror))

                if(line_count > 5000): break

            
        line_count += 1

        

if __name__ == '__main__':

    ekf = EKF.EKF(dt = 0.02, qqgain=0.01, qbgain=100, rgain=0.1)

    read_case("data/testdata.csv","data/testout_Q0001R01.csv",ekf)
