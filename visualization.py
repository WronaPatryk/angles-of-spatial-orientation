import matplotlib.pyplot as plt
import numpy as np
import csv
import errors 

def scatter_hist(x, y, ax, ax_histx, ax_histy, binwidth):

    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    mean_x = np.mean(x)
    mean_y = np.mean(y)

    std_x = np.std(x)
    std_y = np.std(y)

    ax.scatter(x, y, s=0.1)
    

    binwidth = binwidth
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
    ax.set_xlabel("X")
    ax.set_ylabel("Y")





def plot_analyse(inpath, binwidth):
    file_reader = csv.reader(open(inpath) , delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    lsterrorX = []
    lsterrorY = []
    for row in file_reader:
        errorX = float(row[0])
        errorY = float(row[1])

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

    scatter_hist(lsterrorX, lsterrorY, ax, ax_histx, ax_histy, binwidth)

    plt.show()

#plot_analyse('data/test2.csv')

#plot_analyse('data/Aoutput.csv', 0.1)
plot_analyse('data/Gtestdata2.csv', 0.01)


def normal_chart_2_time(inpath, Y1, Y2, Y1t, Y2t, params):

    file_reader = csv.reader(open(inpath) , delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    lstX = []
    lstY = []
    linecount = 0
    time = []
    for row in file_reader:
        linecount += 1

        errorX = float(row[Y1])
        errorY = float(row[Y2])

        lstX.append(errorX)
        lstY.append(errorY + errors.cape_error2(errorX, errorY) * params[0])

        time.append(linecount)

    plt.style.use('bmh')
    plt.figure(figsize = (10,10))

    plt.plot( time, lstX, linestyle='-',color='black', markerfacecolor='black', marker='.', markeredgecolor="black", markersize=5)
    plt.plot( time, lstY, linestyle='-',color='red', markerfacecolor='red', marker='.', markeredgecolor="red", markersize=5)

    plt.legend([Y1t,Y2t], loc = 1)
    plt.xlabel("TIME[s]")
    plt.ylabel(params[4])

    plt.ylim(params[1],params[2])
    plt.xlim(0,linecount)

    plt.title(params[5])

    plt.show()

normal_chart_2_time('data/test2.csv', 2, 5,"ROLL", "ROLL*", [0,0,90, 0, "DEG", "ROLL, ROLL*"])
    

normal_chart_2_time('data/test2.csv', 2, 5,"ROLL", "ROLL*+ BW * 1000", [1000,0,90, 0, "DEG", "ROLL, ROLL* + BW * 1000"])

normal_chart_2_time('data/test2.csv', 1 ,4, "PITCH", "PITCH*", [0,-0.1,0.1, 0, "DEG", "PITCH, PITCH*"])

def normal_chart_1_time(inpath, Y1, Y1t,  params):
    file_reader = csv.reader(open(inpath) , delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    lstX = []
    linecount = 0
    time = []
    for row in file_reader:
        linecount += 1

        errorX = float(row[Y1])

        lstX.append(errorX*params[0])

        time.append(linecount)

    plt.style.use('bmh')
    plt.figure(figsize = (10,10))

    plt.plot( time, lstX, linestyle='-',color='black', markerfacecolor='black', marker='.', markeredgecolor="black", markersize=5)

    plt.legend([Y1t], loc = 1)
    plt.xlabel("TIME[s]")
    plt.ylabel(params[4])

    plt.ylim(params[1],params[2])
    plt.xlim(0,linecount)

    plt.title(params[5])

    plt.show()

normal_chart_1_time('data/test2.csv', 8, "E_ROLL%", [100,-2,2, 0, "BŁĄD WZGĘDNY[%]", "E_ROLL%"])



def normal_chart_move(inpath, Y1, Y2, Y1t, Y2t, params):
    file_reader = csv.reader(open(inpath) , delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    lstX = []
    lstY = []

    for row in file_reader:

        errorX = float(row[Y1])
        errorY = float(row[Y2])

        lstX.append(errorX)
        lstY.append(errorY)


    plt.style.use('bmh')
    plt.figure(figsize = (10,10))

    plt.plot( lstY, lstX, linestyle='-',color='black', markerfacecolor='black', marker='.', markeredgecolor="black", markersize=5)

    plt.legend([Y1t], loc = 1)
    plt.xlabel(params[6])
    plt.ylabel(params[4])

    plt.ylim(params[1],params[2])
    plt.xlim(-0.1,0.1)

    plt.title(params[5])

    plt.show()

normal_chart_move('data/test2.csv', 5, 4, "","", [1,-100,100, 0, "ROLL*", "ROLL*(PITCH*)", "PITCH*" ])