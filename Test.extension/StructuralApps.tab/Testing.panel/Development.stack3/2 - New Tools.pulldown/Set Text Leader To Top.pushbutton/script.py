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

__doc__ = 'For all text in current view (set leaders to top right attachment'

import sys
from Autodesk.Revit.UI import TaskDialog
from System.Collections.Generic import List

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

import clr
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI') 
from Autodesk.Revit.DB import * 

curview = uidoc.ActiveGraphicalView
textnotes = FilteredElementCollector(doc, curview.Id).OfCategory(BuiltInCategory.OST_TextNotes).WhereElementIsNotElementType().ToElementIds()
t = Transaction(doc, 'Set Leaders for Text Elements.')
t.Start()
for item in textnotes:
    el = doc.GetElement(item)
    el.LeaderRightAttachment = LeaderAtachement.TopLine
t.Commit()
TaskDialog.Show("title", str(len(textnotes)))
