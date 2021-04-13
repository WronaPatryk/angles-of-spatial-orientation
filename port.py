import serial
import time
from threading import Thread

def disect_output(s):
    print([ float(x) for i, x in enumerate(str(s).replace('g', '').split(' '))  if i % 2 != 0 ])

class SerialRead:
    def __init__(self, serial_port = '', serial_baud = ''):
        self.sp = serial_port
        self.sb = serial_baud

        self.thread = None

        self.rec = False    # IS RECEIVING
        self.run = True     # IS RUNNING


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
                disect_output(self.sc.readline())

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