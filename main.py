from os import error
import tests as t
import csv
import EKF as EKF
import numpy as np
import errors


def approx_error(real, sim):
    def apx(x,y):
        return abs((x-y)/x)
    return (apx(real[0], sim[0]),apx(real[1], sim[1]), apx(real[2], sim[2]) )


def cape_error(real,sim):
    def apx(x,y):
        return (x-y)/x
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

                rangles = (float(row[3]), float(row[1]) , float(row[2]))

                # Ax = float(row[4])
                # Ay = float(row[5])
                # Az = float(row[6])

                
                # P = float(row[7])
                # Q = float(row[8])
                # R = float(row[9])

                #rangles = (float(row[3]), float(row[1]) , float(row[2]))

                ekf.predict([P , Q , R ])
                ekf.update([Ax, Ay, Az])

                num = EKF.getEulerAngles(ekf.xHat[0:4])

                aerror = approx_error(rangles, num)
                cerror = errors.cape_error(rangles,num)

                print('------------------------------')
                print('Time: %.5f sek; dt: %.5f sek' %(time, dt))
                print('Gx: %.5f rad/s; Gy: %.5f rad/s; Gz: %.5f rad/s' % (P, Q, R))
                print('Ax: %.5fg; Ay: %.5fg; Az: %.5fg' % (Ax, Ay, Az))
                print('Yaw: %.5f; Pitch: %.5f; Roll: %.5f' % num)
                print('RYaw: %.5f; RPitch: %.5f; RRoll: %.5f' %  rangles)
                print('EYaw: %.5f; EPitch: %.5f; ERoll: %.5f' %   cerror )

                file_writer.writerow([time]+ list(num) + list(rangles) + list(cerror))

                if(line_count > 2000): break

            
        line_count += 1

import matplotlib.pyplot as plt

def scatter_hist(x, y, ax, ax_histx, ax_histy):
    # no labels
    ax_histx.tick_params(axis="x", labelbottom=True)
    ax_histy.tick_params(axis="y", labelleft=True)

    mean_x = np.mean(x)
    mean_y = np.mean(y)

    std_x = np.std(x)
    std_y = np.std(y)

    # the scatter plot:
    ax.scatter(x, y, s=1)
    

    # now determine nice limits by hand:
    binwidth = 0.01
    xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
    lim = (int(xymax/binwidth) + 1) * binwidth

    bins = np.arange(-lim, lim + binwidth, binwidth)
    
    ax_histx.hist(x, bins=bins)
    ax_histx.axvline(linewidth=1, color='black')
    

    ax_histy.hist(y, bins=bins, orientation='horizontal')
    ax_histy.axhline(linewidth=1, color='black')

    ax.axhline(linewidth=1, color='black')
    ax.axvline(linewidth=1, color='black')

    ax_histy.axhline(y=mean_y, linewidth=1, color='#d62728')
    ax_histx.axvline(x=mean_x, linewidth=1, color='#d62728')

    ax_histx.set_title(r'$\mu=%.5f$, $\sigma=%.5f$' % (mean_x, std_x))
    ax_histy.set_title(r'$\mu=%.5f$, $\sigma=%.5f$' % (mean_y, std_y))
    
    ax.scatter(mean_x, mean_y, c='red', s=50, marker='x')
    ax.set_xlabel("errorX")
    ax.set_ylabel("errorY")




def plot_analyse(inpath):
    file_reader = csv.reader(open(inpath) , delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    lsterrorX = []
    lsterrorY = []
    for row in file_reader:
        errorX = float(row[8])
        errorY = float(row[9])

        lsterrorX.append(errorX)
        lsterrorY.append(errorY)



    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    spacing = 0.005


    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.2]
    rect_histy = [left + width + spacing, bottom, 0.2, height]


    fig = plt.figure(figsize=(8, 8))

    ax = fig.add_axes(rect_scatter)
    ax_histx = fig.add_axes(rect_histx, sharex=ax)
    ax_histy = fig.add_axes(rect_histy, sharey=ax)

    scatter_hist(lsterrorX, lsterrorY, ax, ax_histx, ax_histy)

    plt.show()




if __name__ == '__main__':

    ekf = EKF.EKF(dt = 0.02, qqgain=0.001, qbgain=0.001, rgain=0.01)

    read_case("data/testdata.csv","data/testout_Q0001R01.csv",ekf)

    #read_case("data/testdata2.csv","data/testout_Q0001R01_2.csv",ekf)

    #plot_analyse("data/testout_Q0001R01.csv")
