#!/usr/bin/env python3

""" Stacking of several data files """

import xpsplot
import matplotlib.pyplot as plt

# simple plots
# --------------
report1 = xpsplot.XPSData.from_file("report1.TXT")

report1.set_column_name("Comp_1", "carb")
report1.set_column_name("Comp_3", "carbonyle")
report1.set_column_name("Comp_4", "tata")
report1.set_column_name("Comp_5", "titi")
report1.set_column_name("Comp_6", "toto")
report1.set_column_name("Comp_7", "tutu")

# or in one shot :
# You must give all columns. If "", column name is keep unchanged
# the first two are KE and Exp
# stuff.set_all_column_names("", "", "carb", "", "carbonyl", "tata", "toto", "titi", "tutu")

# Column that will appear in the plot
toplot = ["Exp", "carb", "titi", "tutu", "envelope"]

# basic or default plot
ax = report1.get_plot(columns=toplot)
plt.show()

# custum plot 1 => add fill and an ylabel
ax = report1.get_plot(
    columns=toplot,
    fill=True,
    ylabel="put here the ylabel you want"
)
plt.show()

# custum plot 2 => change colors, add frame border and move legend
COLORS = ["#333333", "#73d216", "#cc0000", "#3465a4", "#75507b"]
ax = report1.get_plot(
    columns=toplot,
    fill=True,
    ylabel="put here the ylabel you want",
    frame=True,
    colors=COLORS,
    legend_kws=dict(loc="upper left")
)
ax.set_title("A title")
plt.show()

# custum plot 3 => change global options
COLORS = ["#333333", "#73d216", "#cc0000", "#3465a4", "#75507b"]
xpsplot.ALPHA = 1
xpsplot.FONTSIZE = 12
xpsplot.SIZE = (6, 4)
ax = report1.get_plot(
    columns=toplot,
    fill=True,
    ylabel="put here the ylabel you want",
    frame=True,
    colors=COLORS
)
ax.set_title("Changing global options")
plt.show()

# changing the font:
# In order to change the font, use rcParams dictionnary.
# Look at the first lines of xpsplot.py
# font = {'family': 'serif'}
# plt.rc('font', **font)

# a stacked plot
# --------------

# set values for global options
xpsplot.ALPHA = .5
xpsplot.FONTSIZE = 18
xpsplot.SIZE = (12, 8)

# load data and set the title
stuff = xpsplot.StackedXPSData("report1.TXT", "report2.TXT", "report2.TXT")
stuff.title = "C1s of a nice surface"

# set column names. If "", column name is keep unchanged
stuff.set_all_column_names("", "", "carb", "", "", "tata", "toto", "titi", "tutu")

# substract background data
stuff.substract_bg()

# normalize data
stuff.normalize()

# slection of new colors
COLORS = ["#333333", "#cc0000", "#3465a4", "#73d216", "#f57900"]

# save the plot
fig = stuff.get_plot(
    columns=["Exp", "carb", "titi", "tutu", "envelope"],  # columns to plot
    fill=True,                                            # fill component
    pos=[284.5, 290.9, 286.5],                            # vertical line positions
    colors=COLORS,                                        # colors
    ylabel="Intensity (a.u.)"                             # ylabels
)

plt.show()
