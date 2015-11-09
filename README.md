# xpsplot

python classes in order to quickly plot XPS data.

This module contains two classes in order to plot XPS data from vms data
files. There is two classes. The first one, `XPSData`, allows to plot one XPS spectra.
The second class, `StackedXPSData`, allows to plot several XPS data one above
another.

## Contents of the files

* xpsplot.py is the module which contains the classes
* read_XPS_data.ipynb contains short examples of how to use xpsplot module
* read_XPS_data_long.ipynb contains details on the implementation
* report.TXT files are the data file in vms format

## Example 1

This is example.py file in order to plot a single XPS data file

```python

import xpsplot

report1 = xpsplot.XPSData.from_file("report1.TXT")

report1.rename("Comp_1", "carb")
report1.rename("Comp_3", "carbonyle")
report1.rename("Comp_4", "tata")
report1.rename("Comp_5", "titi")
report1.rename("Comp_6", "toto")
report1.rename("Comp_7", "tutu")

report1.save_plot("report1.png", columns=["Exp", "carb", "titi", "tutu"],
                  fill=True, fname=False)
```

this is the output on `report1.png` file :

![example1](report1.png)

## Example 2

This is example2.py file in order to plot several data files

```python
import xpsplot

stuff = xpsplot.StackedXPSData("report1.TXT", "report2.TXT", "report2.TXT")

stuff.title = "C1s of a nice surface"
stuff.set_all_column_names("", "", "carb", "", "", "tata", "toto", "titi", "tutu", "", "")

stuff.save_plot("stack.png", columns=["Exp", "carb", "titi", "tutu"], fill=True,
                pos=[284.5, 290.9, 286.5])
```

this is the output on `stack.png` file :

![example2](stack.png)