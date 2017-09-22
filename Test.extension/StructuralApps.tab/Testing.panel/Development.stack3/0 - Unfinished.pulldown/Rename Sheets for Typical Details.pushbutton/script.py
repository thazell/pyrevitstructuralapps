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
allviews = filter(lambda x: (x.get_Parameter(BuiltInParameter.VIEWPORT_SHEET_NUMBER).HasValue),allviews)


trans = Transaction(doc,"Change Sheet Names")

trans.Start()

with open(csvfilename, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        for s in allsheets:
            sheetnumber = s.get_Parameter(BuiltInParameter.SHEET_NUMBER).AsString()
            sheetname = s.get_Parameter(BuiltInParameter.SHEET_NAME).AsString()
            if s.get_Parameter(BuiltInParameter.SHEET_NUMBER).AsString() == row[0]:
                print row[0]  + " = " + sheetnumber + "NewSheetNumber" + row[2]
                s.get_Parameter(BuiltInParameter.SHEET_NAME).Set(row[1])
                s.get_Parameter(BuiltInParameter.SHEET_NUMBER).Set(row[2])
                viewids = s.GetAllViewports()
                view = doc.GetElement(viewids[0])
                view.get_Parameter(BuiltInParameter.VIEW_DESCRIPTION).Set(row[1])
                

trans.Commit()