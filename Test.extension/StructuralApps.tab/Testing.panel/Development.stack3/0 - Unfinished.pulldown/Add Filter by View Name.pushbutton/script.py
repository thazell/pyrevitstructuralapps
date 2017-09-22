"""
Copyright (c) 2014-2016 Gui Talarico
Written for pyRevit
TESTED API: 2015 | 2016

Copyright (c) 2014-2017 Ehsan Iran-Nejad
Python scripts for Autodesk Revit
TESTED API: 2015 | 2016

Copyright (c) 2014-2017 Timon Hazell
Python scripts for Autodesk Revit
TESTED API: 2015 | 2016

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

# Original Code by dp-stuff.org
# http://dp-stuff.org/revit-view-underlay-property-python-problem/


from Autodesk.Revit.UI import TaskDialog

from scriptutils.userinput import SelectFromList
from scriptutils import logger, this_script

import clr

from System.Collections.Generic import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

def getNames(z_element):
	z_elementname = []
	for e in z_element:
		z_elementname.append(e.Name)
	return z_elementname
	


views = []
baseid = "802532"
baseview = doc.GetElement(ElementId(int(baseid)))

#TaskDialog.Show("Original View",baseview.Name)

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
        elif view.ViewType == ViewType.DraftingView:
            viewlist.append(view)
ids = []


options = sorted(getNames(viewlist))
if options:
    selected_fromlist = SelectFromList.show(options)
    logger.debug('Selected symbols are: {}'.format(selected_fromlist))
    if selected_fromlist:
        if len(selected_fromlist)==1:
            for item in selected_fromlist:
                for t in viewlist:
                    if item == t.Name:
                        baseview = t
                        TaskDialog.Show('BaseView', t.Name)
        else:
            TaskDialog.Show('pyRevit', 'You must select only one template to grab filters.')
            sys.exit
else:
    TaskDialog.Show('pyRevit', 'You must select one item')


options = sorted(getNames(viewlist))

if options:
    selected_fromlist = SelectFromList.show(options)
    logger.debug('Selected symbols are: {}'.format(selected_fromlist))
    if selected_fromlist:
        for item in selected_fromlist:
            for t in viewlist:
                if item == t.Name:
                    views.append(t)
                    #TaskDialog.Show('pyRevit', 'Appended T to views.')
    else:
            TaskDialog.Show('pyRevit', 'Unable to execute application.')
else:
    TaskDialog.Show('pyRevit', 'You must select one item')
    
filters = baseview.GetFilters() # Get all the filter ids

trans = Transaction(doc,"SetFilters")

trans.Start();
for v in views:
	for f in filters:
		if v.IsFilterApplied(f):
			#TaskDialog.Show("Modified View","True")
			overridesettings = baseview.GetFilterOverrides(f)
			v.SetFilterOverrides(f,overridesettings)
		else:
			#TaskDialog.Show("Modified View","False")
			v.AddFilter(f)
			overridesettings = baseview.GetFilterOverrides(f)
			v.SetFilterOverrides(f,overridesettings)
	#rgbList = []
	#for f in filters:
#		filterObject = v.GetFilterOverrides(f)
#		col = filterObject.ProjectionLineColor#
#		if col.IsValid:
#			rgb = DSCore.Color.ByARGB(255, col.Red, col.Green, col.Blue)
#		else:
#			rgb = None
#		rgbList.Add( rgb )
#	colList.Add(rgbList)
trans.Commit()
TaskDialog.Show('pyRevit', 'Check to see if it is complete')
            
"""
collector = FilteredElementCollector(doc)
views = collector.OfClass(View).ToElementsIds()
x = 0
for i in views:
	x=x+1

#TaskDialog.Show("Title",str(x))


#views.append(uidoc.ActiveView)
for v in views:
	filters = v.GetFilters() # Get all the filter ids
	
	rgbList = []
	for f in filters:
		filterObject = v.GetFilterOverrides(f)
		col = filterObject.ProjectionLineColor
		if col.IsValid:
			rgb = DSCore.Color.ByARGB(255, col.Red, col.Green, col.Blue)
		else:
			rgb = None
		rgbList.Add( rgb )
	colList.Add(rgbList)

TaskDialog.Show("Title",''.join(str(e) for e in views))


selection = uidoc.Selection
selection_ids = selection.GetElementIds()

if selection_ids.Count > 0:
    t = Transaction(doc, 'Batch Set Underlay to None')
    t.Start()

    for element_id in selection_ids:
        element = doc.GetElement(element_id)
        if element.Category.Id.IntegerValue == int(BuiltInCategory.OST_Views) \
                and (element.CanBePrinted):
            p = element.get_Parameter(BuiltInParameter.VIEW_UNDERLAY_ID)
            if p is not None:
                p.Set(ElementId.InvalidElementId)

    t.Commit()
else:
    TaskDialog.Show('Remove Underlay', 'Select Views to Remove Underlay')

__window__.Close()
"""