#!/usr/bin/env python3
# coding: utf-8

"""
This module implements two classes in order to quickly plot XPS data.
"""

__author__ = "Germain Salvato-Vallverdu"
__version__ = '0.1'
__email__ = 'germain.vallverdu@univ-pau.fr'
__date__ = '9/11/2015'

import matplotlib
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import re
import os

# plot parameters
font = {'family': 'serif'}
plt.rc('font', **font)

# global options
SIZE = (12, 8)
XLABEL = "Bindig Energy (eV)"
YLABEL = "CPS"
GRID = False
LINEWIDTH = 2
FONTSIZE = 20
ALPHA = .5
COLORS = ["black", "red", "green", "blue", "violet", "orange",
          "cyan", "magenta", "indigo", "maroon", "turquoise"]

# COLORS = ["#cc0000", "#3465a4",  "#f57900", "#c17d11", "#73d216", "#edd400", "#75507b"]
# COLORS = ["black", "blue", "#f57900", "(.0, .6, .0)", "red"]


class XPSData(object):
    """ Manage XPS Data """

    def __init__(self, filename, data, title, path=None, source=-1):
        """
        Build the object. Use this method only if you really know what you are
        doing.
        A better choice is to use XPSData.from_file() method.
        """
        self.data = data
        self.title = title
        self.path = path
        self.source = source
        self.filename = filename
        self._to_plot = []

    def list_columns(self, to_print=True):
        """ print names of component in data """
        if to_print:
            print("\n".join(self.data.columns))
        else:
            return self.data.columns.tolist()

    def set_columns_to_plot(self, *args):
        """ Set names of the columns to be present on the plot """
        for arg in args:
            if arg not in self.data.columns:
                raise NameError("'{}' is not an existing column. ".format(arg) +
                                "Try list_columns()")
        self._to_plot = args

    def set_column_name(self, oldname, newname):
        """
        Rename column `oldname` of pandas table with name `newname`

        Args:
            oldname (str): name of the existing column
            newname (str): new name of the column
        """
        if oldname not in self.data.columns:
            raise NameError("'{}' is not an existing column. ".format(oldname) +
                            "Try list_columns()")
        else:
            self.data.rename(columns={oldname: newname}, inplace=True)

    def set_column_names_interac(self):
        """ Rename column name interactively """
        print("Enter the new column name if needed or return:")
        for c in self.data.columns:
            newname = input("{} => ".format(c))
            if newname.strip() != "":
                self.set_column_name(c, newname)

    def set_all_column_names(self, *args):
        """
        Rename all columns in one shot. If you do not want to rename a column,
        pass "" as argument. The column names are changed from the first column
        to the last depending on how many names you give as arguments.
        """
        for new, old in zip(args, self.data.columns):
            if new != "":
                self.set_column_name(old, new)

    def substract_bg(self, bg="BG"):
        """
        Substract background column to all data columns. If from_file was used
        the background column is called 'BG'. A different column name can be
        given as an optional argument.

        Args:
            bg (str): background column name, default is "BG"
        """
        if bg not in self.data.columns:
            raise NameError("'{}' is not an existing column. ".format(bg) +
                            "Try list_columns()")
        bg_data = self.data[bg].copy()
        for col in self.data.columns:
            self.data[col] -= bg_data

    def normalize(self, BE="Exp", method="minmax"):
        """
        Normalize data by dividing all components by the max value of the data.

        Args:
            BE (str): Column name to use in order to compute the normalization factor
        """
        if BE not in self.data.columns:
            raise NameError("'{}' is not an existing column. ".format(BE) +
                            "Try list_columns()")

        minBE = self.data[BE].min()
        maxBE = self.data[BE].max()

        for col in self.data.columns:
            self.data[col] = (self.data[col] - minBE) / (maxBE - minBE)

    def get_plot(self, columns=None, fill=False, ax=None, xaxes=True,
                 legend=True, colors=COLORS, ylabel=None, frame=False,
                 legend_kws={}):
        """
        Return a matplotlib plot of XPS data for the specified columns.

        Args:
            columns: list of column names to plot
            fill: if True, component are filled (default is False)
            ax: the current instance of a matplotlib Axes
            xaxes: if True, the xaxis is drawn (default is True)
            legend: if True, the legend is present (default is Trye)
            colors: A list of colors as string, the first color is used for enveloppe
                    and exp data
            ylabel: ylabel of the plot (default name of the data file)
            frame: if True, the frame of the plot is drawn (default is False)
            legend_kws: dict of parameters for the legend

        Returns:
            ax: a matplotlib axis object
        """

        # check column names
        if columns:
            for c in columns:
                if c not in self.data.columns:
                    raise NameError("'{}' is not an existing column. ".format(c) +
                                    "Try list_names()")
        elif self._to_plot:
            columns = self._to_plot
        else:
            columns = self.data.columns

        # set up axes
        if not ax:
            fig = plt.figure(figsize=SIZE)
            ax = fig.add_subplot(111)

        # manage colors : first is for enveloppe and exp data
        #                 following colors for components
        first_color = colors[0]
        used_colors = colors[1:]

        # add plots
        ic = 0
        for col in columns:
            if col == "envelope":
                ax.plot(self.data.index, self.data.envelope,
                        linewidth=1, c=first_color, label="")
            elif col == "Exp":
                ax.plot(self.data.index, self.data.Exp, c=first_color, linestyle="",
                        label="Exp", marker="o", markersize=4.)
            else:
                color = used_colors[ic % len(used_colors)]
                if fill and "BG" in self.data.columns:
                    ax.fill_between(self.data.index, self.data.BG,
                                    self.data[col], label=col, alpha=ALPHA,
                                    color=color)
                else:
                    ax.plot(self.data.index, self.data[col], linewidth=LINEWIDTH,
                            c=color, label=col)
                ic += 1

        # plot options :
        #   * remove frame and manage spines
        # ax.set_frame_on(False)
        [spine.set_linewidth(2) for spine in ax.spines.values()]
        [ax.spines[k].set_visible(frame) for k in ["top", "left", "right"]]
        #   * remove y ticks
        ax.set_yticks([])
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=FONTSIZE)
        else:
            ax.set_ylabel(self.filename, fontsize=FONTSIZE)
        #   * revert x axes
        ax.set_xlim((self.data.index.max(), self.data.index.min()))
        #   * draw x axes
        if xaxes:
            ax.set_xlabel(XLABEL, fontsize=FONTSIZE)
            ax.tick_params(width=2, labelsize=FONTSIZE)
            ax.get_xaxis().tick_bottom()
        else:
            ax.get_xaxis().set_visible(False)
            ax.spines["bottom"].set_visible(False)
        #   * add grid
        ax.grid(GRID)
        #   * add legend
        if legend:
            ax.legend(fontsize=FONTSIZE, **legend_kws)

        return ax

    def save_plot(self, filename="plot.pdf", columns=None, fill=False,
                  legend=True, ylabel=None, colors=COLORS, frame=False,
                  legend_kws={}):
        """
        Save matplotlib plot to a file.

        Args:
            filename: Filename to write to.
            columns: list of column names to plot
            fill: if True, component are filled
            legend: if True, the legend is present
            colors: A list of colors as string, the first color is used for the
                    enveloppe and Exp data
            ylabel: ylabel of the plot (default name of the data file)
            frame: if True, the frame of the plot is drawn (default is False)
            legend_kws: dict of parameters for the legend
        """
        ax = self.get_plot(columns=columns, fill=fill, legend=legend,
                           ylabel=fname, colors=colors, frame=frame,
                           legend_kws=legend_kws)
        plt.savefig(filename)

    @staticmethod
    def from_file(filename):
        """ return a XPSData object from a vms file extracted from CasaXPS. """
        # read the header
        with open(filename, "r") as f:
            path = f.readline().strip()
            title = f.readline().strip()
            source = float(re.findall("(\d+.\d+)", f.readline())[0])
            header = f.readline().split("\t")

        # read data
        num_data = np.loadtxt(filename, skiprows=4, dtype=np.float64)

        # build pandas table
        ndata = len(header)
        index = num_data[:, 1]
        data = num_data[:, [0] + list(range(2, ndata))]
        columns = ["KE", "Exp"]
        columns += ["Comp_{}".format(i - 2) for i in list(range(3, ndata - 2))]
        columns += ["BG", "envelope"]

        data_frame = pd.DataFrame(data=data, index=index, columns=columns)

        return XPSData(filename, data_frame, title, path, source)

    def __str__(self):
        line = "filename : {}\n".format(self.filename)
        line += "path     : {}\n".format(self.path)
        line += "title    : {}\n".format(self.title)
        line += "source   : {} eV\n".format(self.source)
        line += "columns  : {}\n".format(" ; ".join(self.data.columns))
        return line


class StackedXPSData(object):
    """ Merge several XPSData on one plot """

    def __init__(self, *args):
        """
        Build the object form a list of path to files which contains the XPS
        data needed to do the plot. The file are assume to be in vms format.

        data = StackedXPSData("data1.vms", "data2.vms"[, ...])
        """
        for arg in args:
            if not os.path.exists(arg):
                raise FileNotFoundError("No such file or directory {}".format(arg))
        self.filenames = args
        self.xpsData = [XPSData.from_file(arg) for arg in args]
        self.title = self.xpsData[0].title
        self._to_plot = []

    def set_columns_to_plot(self, *args):
        """ Set names of the columns to be present on the plot """
        self._to_plot = args

    def list_columns(self, to_print=True):
        """ List all column names """
        if to_print:
            for xps in self.xpsData:
                print("{} : {}".format(xps.title, xps.filename))
                print(40 * "-")
                print(" ; ".join([c for c in xps.data.columns]) + "\n")
        else:
            return [xps.data.columns.tolist() for xps in self.xpsData]

    def set_column_name(self, oldname, newname):
        """
        Change the name of the column oldname in newname for all data.
        """
        for xpsData in self.xpsData:
            xpsData.set_column_name(oldname, newname)

    def set_all_column_names(self, *args):
        """
        Rename all columns in one shot. You must give a name for
        all columns.
        """
        for xpsData in self.xpsData:
            xpsData.set_all_column_names(*args)

    def set_column_names_interac(self):
        """
        Rename column name interactively, assume all XPSData have got the same
        column names.
        """
        print("Enter the new column name if needed or return:")
        for c in self.xpsData[0].data.columns:
            newname = input("{} => ".format(c))
            if newname.strip() != "":
                self.set_column_name(c, newname)

    def substract_bg(self, bg="BG"):
        """
        Substract the background column given as bg arguments to all data
        columns in each xpsData object.

        Args:
            bg (string): name of the background column, default is "BG"
        """
        for xpsData in self.xpsData:
            xpsData.substract_bg(bg)

    def normalize(self, BE="Exp"):
        """
        Normalize data by dividing all components by the max value of the data.

        Args:
            BE (str): Column name to use in order to compute the normalization factor
        """
        for xpsData in self.xpsData:
            xpsData.normalize(BE)

    def get_plot(self, columns=None, fill=False, legend=True, ylabel=None,
                 pos=[], colors=COLORS, legend_kws={}):
        """
        Return a matplotlib plot of all XPS data for the specified columns.
        XPS data are stacked with the first file at the top and the last
        file at the bottom.

        The legend is added to the top axes.

        Args:
            columns: list of column names to plot
            fill: if True, component are filled
            legend: if True, the legend is present on the top plot
            ylabel: ylabel of the plot (default name of the data file)
            colors: A list of colors as string, the fist color is used for the
                    enveloppe and the Exp data.
            pos: list of x position (in eV) of vertical lines if needed
            legend_kws: dict of parameters for the legend

        Returns:
            fig: a matplotlib figure object
        """
        if self._to_plot:
            columns = self._to_plot

        # make subplots
        fig, axis = plt.subplots(len(self.xpsData), sharex=True, sharey=True)
        fig.set_size_inches(SIZE[1], SIZE[0])
        fig.subplots_adjust(hspace=0)

        # add plot using XPSData.get_plot to each subplots
        for axes, xps in zip(axis[:-1], self.xpsData[:-1]):
            xps.get_plot(columns, fill, ax=axes, xaxes=False, legend=False,
                         ylabel=ylabel, colors=colors, frame=True)
        # last plot with xaxis
        self.xpsData[-1].get_plot(columns, fill, ax=axis[-1], legend=False,
                                  ylabel=ylabel, colors=colors, frame=True)

        # the legend
        if legend:
            axis[0].legend(fontsize=FONTSIZE, **legend_kws)

        # figure title
        fig.suptitle(self.title)

        # add vertical lines to a given position
        for i, axes in enumerate(axis):
            for p in pos:
                ymin, ymax = axis[0].get_ylim()
                axes.axvline(x=p, ymin=ymin, ymax=ymax, c="#555753",
                             linewidth=2, clip_on=True)
                if i == 0:
                    axes.text(x=p, y=ymax, s="{:5.1f}".format(p),
                              fontsize=FONTSIZE / 1.5,
                              verticalalignment="bottom",
                              horizontalalignment='center')

        return fig

    def save_plot(self, filename="plot.pdf", columns=None, fill=False, legend=True,
                  ylabel=None, pos=[], colors=COLORS, legend_kws={}):
        """
        Save matplotlib plot to a file.

        Args:
            filename: Filename to write to.
            columns: list of column names to plot
            fill: if True, component are filled
            legend: if True, the legend is present on the top plot
            ylabel: ylabel of the plot (default name of the data file)
            colors: A list of colors as string
            pos: list of x position (in eV) of vertical lines if needed.
            legend_kws: dict of parameters for the legend
        """
        fig = self.get_plot(columns, fill, legend, ylabel, pos, colors, legend_kws)
        fig.savefig(filename)

    def __str__(self):
        line = self.title + "\n" + 30 * "-" + "\n"
        line += "\n".join([str(xps) for xps in self.xpsData])
        return line
