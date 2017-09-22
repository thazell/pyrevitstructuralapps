"""
Copyright Silman 2017

pyRevit is a free set of scripts for Autodesk Revit: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See this link for a copy of the GNU General Public License protecting this package.
https://github.com/eirannejad/pyRevit/blob/master/LICENSE
"""

__doc__ = 'This command will set columns as a higher priority when joining with walls.  Walls will be cut, columns will remain in full size.  This helps the graphical column schedule.'

import sys
from Autodesk.Revit.UI import TaskDialog
from System.Collections.Generic import List

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
import sys
import clr

import numpy as np

clr.AddReference('RevitAPIUI') 
from Autodesk.Revit.DB import * 

def closest_node(node, nodelist):
    nodelist = np.asarray(nodelist)
    deltas = nodelist - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.argmin(dist_2)



nodes = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_AnalyticalNodes).WhereElementIsNotElementType().ToElements()
TaskDialog.Show("Number of nodes selected", "nodes - " + str(len(nodes)))
display = "Look at this"
for n in nodes:
    if "ReferencePoint" in n.ToString():
        zpoint = n.Position
        display += str(zpoint.X) + " " + str(zpoint.Y) + " "  + str(zpoint.Z) + "\n"
        #TaskDialog.Show("header",str(n.X) + str(n.Y) + str(n.Z))
        display += str(closest_node(n,nodes))
TaskDialog.Show("header",display)

sys.exit
