#!/usr/bin/env python3

""" Simple plot of one XPS data file """

import xpsplot

report1 = xpsplot.XPSData.from_file("report1.TXT")

report1.set_column_name("Comp_1", "carb")
report1.set_column_name("Comp_3", "carbonyle")
report1.set_column_name("Comp_4", "tata")
report1.set_column_name("Comp_5", "titi")
report1.set_column_name("Comp_6", "toto")
report1.set_column_name("Comp_7", "tutu")

report1.save_plot("report1.png", columns=["Exp", "carb", "titi", "tutu"],
                  fill=True, fname=False)
