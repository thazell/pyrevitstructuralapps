"""
Copyright (c) 2014-2017 Timon Hazell
Python scripts for Autodesk Revit
TESTED API: 2018

Based heavily on code from Ehsan Iran-Nejad and Gui Talarico

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

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

collector = FilteredElementCollector(doc)
allviews = collector.OfClass(View).ToElements()
allassemblies = collector.OfClass(Assembly).ToElements()

print allassemblies

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

            
            """
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