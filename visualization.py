import matplotlib.pyplot as plt
import numpy as np
import csv

def scatter_hist(x, y, ax, ax_histx, ax_histy):

    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    mean_x = np.mean(x)
    mean_y = np.mean(y)

    std_x = np.std(x)
    std_y = np.std(y)

    ax.scatter(x, y, s=0.1)
    

    binwidth = 1
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
        errorX = float(row[1])
        errorY = float(row[2])

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

plot_analyse('data/test2.csv')