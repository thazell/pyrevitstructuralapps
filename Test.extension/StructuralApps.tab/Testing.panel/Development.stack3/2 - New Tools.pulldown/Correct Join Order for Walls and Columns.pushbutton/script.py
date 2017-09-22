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

import clr

from Autodesk.Revit.DB import * 

walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElementIds()
columns = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElementIds()
TaskDialog.Show("Number of Walls and Columns Selected", "Walls - " + str(len(walls)) + " Columns - " + str(len(columns)))
results = []
t = Transaction(doc, 'Switch Join Between all Columns and Walls')
t.Start()
i = 0
for c in columns:
    cel = doc.GetElement(c)
    for w in walls:
        try:
            wel = doc.GetElement(w)
            if JoinGeometryUtils.AreElementsJoined(doc,wel,cel):
                if JoinGeometryUtils.IsCuttingElementInJoin(doc,wel,cel):
                    result = JoinGeometryUtils.SwitchJoinOrder(doc,wel,cel)
                    results.append(result)
                    print result
                    #TaskDialog.Show("title", str(i))
                    i+=1
        except:
            TaskDialog.Show("title", str(i))
            i+=1
            pass
# t = Transaction(doc, 'Set Leaders for Text Elements.')
# t.Start()
# for item in textnotes:
    # el = doc.GetElement(item)
    # el.LeaderRightAttachment = LeaderAtachement.TopLine
t.Commit()
# TaskDialog.Show("title", str(len(textnotes)))
