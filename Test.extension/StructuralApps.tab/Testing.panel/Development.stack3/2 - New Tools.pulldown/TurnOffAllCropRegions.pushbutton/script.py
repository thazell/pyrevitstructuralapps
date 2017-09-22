"""
Copyright (c) 2014-2016 Timon Hazell
Written for pyRevit
TESTED API: 2015 | 2016

pyRevit is a free set of scripts for Autodesk Revit: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

# Original Code by dp-stuff.org
# http://dp-stuff.org/revit-view-underlay-property-python-problem/
import clr
from Autodesk.Revit.UI import TaskDialog

from scriptutils.userinput import SelectFromList
from scriptutils import logger, this_script

from System.Collections.Generic import *


doc = __revit__.ActiveUIDocument.Document

collector = FilteredElementCollector(doc)
allviews = collector.OfClass(View).ToElements()
templatelist = []
viewlist = []

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

trans = Transaction(doc,"SetFilters")

trans.Start();
for v in viewlist:
    isVisbileParameter = v.get_Parameter(BuiltInParameter.VIEWER_CROP_REGION_VISIBLE);
    isVisbileParameter.Set(0);
trans.Commit()
TaskDialog.Show('pyRevit', 'Check to see if it is complete')
