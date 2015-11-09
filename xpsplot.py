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
font = {'family': 'serif', 'size': 20}
plt.rc('font', **font)

SIZE = (12, 8)
XLABEL = "Bindig Energy (eV)"
YLABEL = "CPS"
GRID = False
LINEWIDTH = 2
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

    def list_columns(self):
        """ print names of component in data """
        [print(c) for c in self.data.columns]

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
        Rename all columns in one shot. You must give a name for
        all columns. If you give "", the column name is not changed.
        """
        if len(args) != len(self.data.columns):
            raise ValueError("You must give all columns name.\n" +
                             "There are {} columns.\n".format(len(self.data.columns)) +
                             "You gave : {}".format(args))
        for new, old in zip(args, self.data.columns):
            if new != "":
                self.set_column_name(old, new)

    def get_plot(self, columns=None, fill=False, ax=None, xaxes=True,
                 legend=True, fname=True):
        """
        Return a matplotlib plot of XPS data for the specified columns.

        Args:
            columns: list of column names to plot
            fill: if True, component are filled
            ax: the current instance of a matplotlib Axes
            xaxes: if True, the xaxis is drawn
            legend: if True, the legend is present
            fname: if True, the name of the data file is written
        """
        if columns:
            for c in columns:
                if c not in self.data.columns:
                    raise NameError("'{}' is not an existing column. ".format(c) +
                                    "Try list_names()")
        elif self._to_plot:
            columns = self._to_plot
        else:
            columns = self.data.columns

        if not ax:
            fig = plt.figure(figsize=SIZE)
            ax = fig.add_subplot(111)

        for i, col in enumerate(columns):
            color = COLORS[i % len(COLORS)]
            if fill and "BG" in self.data.columns and col != "Exp":
                ax.fill_between(self.data.index, self.data.BG, self.data[col],
                                alpha=ALPHA, color=color)
            ax.plot(self.data.index, self.data[col], linewidth=LINEWIDTH,
                    c=color, label=col)

        # plot options :
        #   * remove frame
        #   * remove y axis
        #   * draw x axes
        ax.set_frame_on(False)
        if fname:
            ax.set_yticks([])
            ax.set_ylabel(self.filename, fontsize=10)
        else:
            ax.get_yaxis().set_visible(False)
        ax.grid(GRID)
        ax.set_xlim((self.data.index.min(), self.data.index.max()))
        if xaxes:
            ymin, ymax = ax.get_ylim()
            xmin, xmax = ax.get_xlim()
            ax.set_xlabel(XLABEL)
            ax.get_xaxis().tick_bottom()
            ax.add_line(matplotlib.lines.Line2D((xmin, xmax), (ymin, ymin),
                                                color="black", linewidth=5.))
        else:
            ax.get_xaxis().set_visible(False)

        if legend:
            ax.legend()

        return ax

    def save_plot(self, filename="plot.pdf", columns=None, fill=False,
                  legend=True, fname=True):
        """
        Save matplotlib plot to a file.

        Args:
            filename: Filename to write to.
            columns: list of column names to plot
            fill: if True, component are filled
            legend: if True, the legend is present
            fname: if True, the file name of the data is written
        """
        ax = self.get_plot(columns=columns, fill=fill, legend=legend, fname=fname)
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

    def list_columns(self):
        """ List all column names """
        for xps in self.xpsData:
            print("{} : {}".format(xps.title, xps.filename))
            print(40 * "-")
            print(" ; ".join([c for c in xps.data.columns]) + "\n")

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

    def get_plot(self, columns=None, fill=False, legend=True, fname=True, pos=[]):
        """
        Return a matplotlib plot of all XPS data for the specified columns.
        XPS data are stacked with the first file at the top and the last
        file at the bottom.

        Args:
            columns: list of column names to plot
            fill: if True, component are filled
            legend: if True, the legend is present
            fname: if True, the name of the data file is written
            pos: list of x position of vertical lines
        """
        if self._to_plot:
            columns = self._to_plot

        # make subplots
        fig, axis = plt.subplots(len(self.xpsData), sharex=True, sharey=True)
        fig.set_size_inches(SIZE[1], SIZE[0])
        fig.subplots_adjust(hspace=0)

        for axes, xps in zip(axis[:-1], self.xpsData[:-1]):
            xps.get_plot(columns, fill, ax=axes, xaxes=False, legend=False, fname=fname)
        self.xpsData[-1].get_plot(columns, fill, ax=axis[-1], legend=False, fname=fname)

        # the legend
        if legend:
            axis[0].legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0.)

        fig.suptitle(self.title)

        for p in pos:
            ymin = -(len(self.xpsData) - 1)
            axis[0].axvline(x=p, ymin=-(len(self.xpsData) - 1), ymax=1.1, c="#555753",
                            linewidth=2, clip_on=False)
            ymin, ymax = axis[0].get_ylim()
            axis[0].text(x=p, y=1.15 * ymax, s="{:5.1f}".format(p), fontsize=12,
                         horizontalalignment='center')

        return fig

    def save_plot(self, filename="plot.pdf", columns=None, fill=False, legend=True,
                  fname=True, pos=[]):
        """
        Save matplotlib plot to a file.

        Args:
            filename: Filename to write to.
            columns: list of column names to plot
            fill: if True, component are filled
            fname: if True, the name of the data file is written
            pos: list of x position of vertical lines
        """
        ax = self.get_plot(columns, fill, legend, fname, pos)
        plt.savefig(filename)

    def __str__(self):
        line = self.title + "\n" + 30 * "-" + "\n"
        line += "\n".join([str(xps) for xps in self.xpsData])
        return line
