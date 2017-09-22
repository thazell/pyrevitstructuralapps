"""
Copyright (c) 2014-2017 Timon Hazell
Python scripts for Autodesk Revit
TESTED API: 2015 | 2016

pyRevit is a free set of scripts for Autodesk Revit: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from Autodesk.Revit.UI import TaskDialog

from scriptutils.userinput import SelectFromList
from scriptutils import logger, this_script
import sys
import clr


from System.Collections.Generic import *

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import csv
csvfilename = "C:/Temp/NewTypicalDetailNames.csv"

def getNames(z_element):
	z_elementname = []
	for e in z_element:
		z_elementname.append(e.Name)
	return z_elementname
	

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

views = []

allsheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()

collector = FilteredElementCollector(doc)
allviews = collector.OfClass(View).ToElements()

viewlist = []
templatelist = []

for view in allviews:
    #if view.ViewType == ViewType.ThreeD:
        if (view.IsTemplate):
            templatelist.append(view)
        elif view.ViewType == ViewType.Elevation:
            viewlist.append(view)
        elif view.ViewType == ViewType.FloorPlan:
            viewlist.append(view)
        elif view.ViewType == ViewType.ThreeD:
            viewlist.append(view)
        elif view.ViewType == ViewType.EngineeringPlan:
            viewlist.append(view)
        elif view.ViewType == ViewType.Section:
            viewlist.append(view)
        elif view.ViewType == ViewType.Detail:
            viewlist.append(view)
        elif view.ViewType == ViewType.DraftingView:
            viewlist.append(view)


trans = Transaction(doc,"Change View Names")

trans.Start()


for v in viewlist:
    oldviewname =  v.get_Parameter(BuiltInParameter.VIEW_NAME).AsString()
    #view.get_Parameter(BuiltInParameter.VIEW_NAME).Set(row[1])
    newviewname = oldviewname.replace(" ", "_")
    newviewname = newviewname.replace("_-_", "-")
    v.get_Parameter(BuiltInParameter.VIEW_NAME).Set(newviewname)       

trans.Commit()