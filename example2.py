#!/usr/bin/env python3

""" Stacking of several data files """

import xpsplot

stuff = xpsplot.StackedXPSData("report1.TXT", "report2.TXT", "report2.TXT")

stuff.title = "C1s of a nice surface"
stuff.set_all_column_names("", "", "carb", "", "", "tata", "toto", "titi", "tutu", "", "")

stuff.save_plot("stack.png", columns=["Exp", "carb", "titi", "tutu"], fill=True,
                pos=[284.5, 290.9, 286.5])
