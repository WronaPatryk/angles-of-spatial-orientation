import serial
import time
from threading import Thread
import EKF as EKF
import numpy as np
from itertools import count
import csv

def disect_output(s):
    return([ float(x) for i, x in enumerate(str(s).replace('g', '').split(' '))  if i % 2 != 0 ])


def getAccelVector(a):
    accel = np.array(a).transpose()
    accelMag = (accel[0] ** 2 + accel[1] ** 2 + accel[2] ** 2) ** 0.5
    return accel / accelMag

class SerialRead:
    def __init__(self, serial_port = '', serial_baud = ''):
        self.sp = serial_port
        self.sb = serial_baud

        self.thread = None

        self.rec = False    # IS RECEIVING
        self.run = True     # IS RUNNING

        self.file_writer = csv.writer(open('data/output.csv', mode='w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        self.YAW = []
        self.PITCH = []
        self.ROLL = []

        self.start_time = 0

        self.ekf = EKF.EKF(getAccelVector([1.00513, -0.01831, 0.19238]), [-0.30534*np.pi/180, -0.81679*np.pi/180, -0.48168*np.pi/180], 0.1)


        print('Trying to connect to: ' + str(serial_port) + ' at ' + str(serial_baud) + ' BAUD.')

        try:
            self.sc = serial.Serial(serial_port, serial_baud, timeout=4)
            print('Connected to ' + str(serial_port) + ' at ' + str(serial_baud) + ' BAUD.')
        except:
            print("Failed to connect with " + str(serial_port) + ' at ' + str(serial_baud) + ' BAUD.')
            exit()

    def start_serial(self):
        if self.thread == None:
            self.thread = Thread(target=self.back_thread)
            self.thread.start()
            while self.rec != True:
                time.sleep(0.1)


    def process_output(self, output):
        self.ekf.predict([output[3]*np.pi/180, output[4]*np.pi/180, output[5]*np.pi/180])
        self.ekf.update([output[0], output[1], output[2]])
        num = EKF.getEulerAngles(self.ekf.xHat[0:4])
        print('------------------------------')
        print('Gx: %.5f; Gy: %.5f; Gz: %.5f' % (output[3], output[4], output[5]))
        print('Ax: %.5f; Ay: %.5f; Az: %.5f' % (output[0], output[1], output[2]))
        print('Yaw: %.5f; Pitch: %.5f; Roll: %.5f' % num)

        self.file_writer.writerow([time.time() - self.start_time]+list(num))


    def back_thread(self):   
            time.sleep(1.0)  
            self.sc.reset_input_buffer()
            self.start_time = time.time()

            while (self.run):
                self.rec = True
                output = disect_output(self.sc.readline())
                #print(output)
                self.process_output(output)
                #print(self.ekf.xHat[4:7])

    def close(self):
        self.run = False
        self.thread.join()
        self.sc.close()
        print('DISCONNECTED')
        

def port_config():
    serial_port = '/dev/ttyACM0'
    #portName = 'COM6'
    serial_baud = 115200

    sr = SerialRead(serial_port,serial_baud)
    sr.start_serial()


port_config()
