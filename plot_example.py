#!/usr/bin/env python3

import xpsplot
import matplotlib.pyplot as plt

# set values for global options
font = {'family': 'sans'}
plt.rc('font', **font)

xpsplot.ALPHA = .5
xpsplot.FONTSIZE = 14

COLORS = ["#333333", "#73d216", "#cc0000", "#3465a4", "#75507b"]

# data files
datafiles = ["report1.TXT", "report2.TXT", "report2.TXT"]

# set up the plot and make subplots
nrows = len(datafiles)
fig, axis = plt.subplots(nrows, sharex=True, sharey=True, figsize=(5, 8))
fig.subplots_adjust(hspace=0)
fig.suptitle("My super title")

for idata, datafile in enumerate(datafiles):

    xpsData = xpsplot.XPSData.from_file(datafile)

    # here, you can do something like:
    # if datafile == "blabla":
    #     do a specific things for that data/sample
    #
    # or other:
    # if idata == 42:
    #     do a specific things
    #
    # here you can manage columns name, columns to plot, work on the data (filtering ...)

    xpsData.substract_bg()
    xpsData.normalize()

    # set column names
    # the first two are KE and Exp
    xpsData.set_all_column_names("", "", "carb", "", "carbonyl", "tata", "toto", "titi", "tutu")

    # Column that will appear in the plot
    toplot = ["Exp", "carb", "titi", "tutu", "envelope"]

    xaxes = False
    if idata == nrows - 1:
        xaxes = True

    # add plot using XPSData.get_plot
    axis[idata] = xpsData.get_plot(
        columns=toplot,
        fill=True,
        ax=axis[idata],
        xaxes=xaxes,
        legend=False,
        ylabel="Intensity (u.a.)",
        colors=COLORS,
        frame=False
    )


# the legend
axis[0].legend(fontsize=12)

# add vertical lines to a given position
pos = [292, 285]
for i, axes in enumerate(axis):
    for p in pos:
        ymin, ymax = axis[0].get_ylim()
        axes.axvline(x=p, ymin=ymin, ymax=ymax, c="#555753",
                     linewidth=2, clip_on=True)
        if i == 0:
            axes.text(x=p, y=ymax, s="{:5.1f}".format(p),
                      fontsize=14,
                      verticalalignment="bottom",
                      horizontalalignment='center')

# do other things

plt.show()
