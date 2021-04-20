import serial
import time
from threading import Thread
import EKF as EKF
import numpy as np

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

        self.ekf = EKF.EKF(getAccelVector([-1.00513, 0.01831, -0.19238]), [-0.30534, -0.81679, -0.38168], 0.1)


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


    def back_thread(self):   
            time.sleep(1.0)  
            self.sc.reset_input_buffer()
            while (self.run):
                self.rec = True
                output = disect_output(self.sc.readline())
                #print(output)
                self.ekf.predict([output[3], output[4], output[5]])
                self.ekf.update([output[0], output[1], output[2]])
                print(EKF.getEulerAngles(self.ekf.xHat[0:4]))
                print(self.ekf.xHat[4:7])

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