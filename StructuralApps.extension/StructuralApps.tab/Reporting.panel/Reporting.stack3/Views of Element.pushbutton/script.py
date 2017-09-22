"""
Modified by Silman

Copyright (c) 2014-2017 Ehsan Iran-Nejad
Python scripts for Autodesk Revit

This file is part of pyRevit repository at https://github.com/eirannejad/pyRevit

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

__doc__ = 'Lists all views in which the selected elements are visible.'
import sys
import datetime

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter, ViewType
from Autodesk.Revit.UI import TaskDialog
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

cl_views = FilteredElementCollector(doc)
allviews = cl_views.OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
views = filter(lambda x: ((x.ViewType != ViewType.DraftingView or x.ViewType != ViewType.ThreeD) and not x.IsTemplate and x.get_Parameter(BuiltInParameter.VIEWPORT_SHEET_NUMBER).HasValue),allviews)

viewList = []
# print str(datetime.datetime.now())
if len(uidoc.Selection.GetElementIds()) > 0:
    for v in views:
        cl_els = FilteredElementCollector(doc, v.Id).WhereElementIsNotElementType().ToElementIds()
        i = 0
        for elId in uidoc.Selection.GetElementIds():
            if elId in cl_els:
                i = + 1
                viewList.append(v)
else:
    TaskDialog.Show("Try Again", "No element was selected, try again.")
    __window__.Close()
    sys.exit()
if len(viewList) > 0:
    print('\n\nSheet views containing the selected elements:')

else: 
    TaskDialog.Show("No views were found", "No views on sheets were found with this element")

myset = set(viewList)
viewList = list(myset)
    
for v in viewList:
    print('{0}{1}ID:{2}'.format(v.ViewName.ljust(45),
                                str(v.ViewType).ljust(25),
                                str(v.Id).ljust(10)))

# print str(datetime.datetime.now())
# if len(uidoc.Selection.GetElementIds()) > 0:
    # for elId in uidoc.Selection.GetElementIds():
        # for v in views:
            # cl_els = FilteredElementCollector(doc, v.Id).WhereElementIsNotElementType().ToElementIds()
            # i = 0
            # if elId in cl_els:
                # i = + 1
                # viewList.append(v)
# else:
    # TaskDialog.Show("Try Again", "No element was selected, try again.")
    
# if len(viewList) > 0:
    # print('\nSheet views containing the selected elements:):')
# else: 
    # TaskDialog.Show("No views were found", "No views on sheets were found with this element")

# myset = set(viewList)
# viewList = list(myset)

# viewListNames = []

# for v in viewList:
    # viewListNames.append(v.ViewName)
# viewListNames = sorted(viewListNames)
# for v in viewListNames:
    # print v

# for v in viewList:
    # print('{0}{1}ID:{2}'.format(v.ViewName.ljust(45),
                                # str(v.ViewType).ljust(25),
                                # str(v.Id).ljust(10)))
                                
# # print "\n" + str(datetime.datetime.now())

# # print str(datetime.datetime.now())
# # if len(uidoc.Selection.GetElementIds()) > 0:
    # # for v in views:
        # # cl_els = FilteredElementCollector(doc, v.Id).WhereElementIsNotElementType().ToElementIds()
        # # i = 0
        # # for elId in uidoc.Selection.GetElementIds():
            # # if elId in cl_els:
                # # i = + 1
                # # viewList.append(v)
# # else:
    # # TaskDialog.Show("Try Again", "No element was selected, try again.")
    # # __window__.Close()
    # # sys.exit()
# # if len(viewList) > 0:
    # # print('\n\nSheet views containing the selected elements:):')

# # else: 
    # # TaskDialog.Show("No views were found", "No views on sheets were found with this element")

# # myset = set(viewList)
# # viewList = list(myset)
    
# # for v in viewList:
    # # print('{0}{1}ID:{2}'.format(v.ViewName.ljust(45),
                                # # str(v.ViewType).ljust(25),
                                # # str(v.Id).ljust(10)))

# # print str(datetime.datetime.now())